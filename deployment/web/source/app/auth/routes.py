# -*- coding=utf-8 -*-
from flask import url_for
from flask_restful import Api, fields, Resource
from flask_restful import reqparse
from flask_restful import marshal_with
from flask_login import login_user, current_user

from app.auth import auth
from app.models import User, LocalAuth
from app.auth.errors import *
from app.auth.email import generate_confirmation_token
from app.auth.email import confirm_token, send_email
from app import db

# login 验证
def login_required(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        return f(*args, **kwargs)
    return decorator

# flask-restful 设置
api = Api(auth)


class LocalRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        # 验证长度
        if len(args['username']) == 0 or len(args['username']) > 32:
            abort_unacceptable_length("username")
        if len(args['email']) == 0:
            abort_unacceptable_length("email")
        if len(args['password']) == 0:
            abort_unacceptable_length("password")
        # User existing
        if LocalAuth.query.filter_by(username=args['username']).first():
            abort_username_existed('username')
        if LocalAuth.query.filter_by(email=args['email']).first():
            abort_username_existed('email')
        # 写入数据库
        user = User()
        db.session.add(user)
        db.session.commit()
        localauth = LocalAuth(username=args['username'],
                              email=args['email'], user=user)
        localauth.hash_password(args['password'])
        db.session.add(localauth)
        db.session.commit()
        # 发送邮件
        token = generate_confirmation_token(localauth.email)
        confirm_url = url_for('frontend.confirm_email',
                              token=token, _external=True)
        html = '''
               <p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p>
               <p><a href="%s">%s</a></p>
               <br>
               <p>Cheers!</p>
               '''%(confirm_url, confirm_url)
        subject = "Please confirm your email"
        send_email(localauth.email, subject, html)
        return "{ 'username': %s }" % (localauth.username), 201


class EmailConirmation(Resource):
    def post(self, token):
        # 验证过期
        try:
            email = confirm_token(token)
        except:
            return 'The confirmation link is invalid or has expired.', 404
        # 数据库读取
        localauth = LocalAuth.query.filter_by(email=email).first()
        if not localauth:
            return 'The confirmation link is invalid or has expired.', 404
        # 确认邮箱
        if localauth.confirmed:
            return "Account already confirmed. Please login.", 200
        else:
            localauth.confirmed = True
            db.session.commit()
            return "You have confirmed your account. Thanks!", 201


class LocalAuthLogin(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        # 验证用户
        localauth =  LocalAuth.query.filter_by(username=args['username']).first()
        if not localauth or not localauth.verify_password(args['password']):
            abort_wrong_login()
        # login
        user = localauth.user
        login_user(user)
        return "login successfully", 200


class RoleChange(Resource):
    method_decorators = [login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('role')
        args = parser.parse_args()
        if not args['role']:
            return current_user.role, 200
        #  转换为int
        if args['role'] == "-1":
            role = -1
        elif args['role'] == "0":
            role = 0
        elif args['role'] == "1":
            role = 1
        elif args['role'] == "2":
            role = 2
        else:
            abort_role_cannot_setting()
        current_user.role = role
        db.session.commit()
        return args['role'], 200


# the Api resource routing
api.add_resource(LocalRegister, '/register')
api.add_resource(LocalAuthLogin, '/login')
api.add_resource(EmailConirmation, '/confirm/<token>')
api.add_resource(RoleChange, '/role')
