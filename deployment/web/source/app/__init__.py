# -*- coding=utf-8 -*-
from flask import Flask, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

from config import config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # register the blueprint
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1.0/auth')

    from app.todo import todo as todo_blueprint
    app.register_blueprint(todo_blueprint, url_prefix='/api/v1.0/todo')

    from app.frontend import frontend as frontend_blueprint
    app.register_blueprint(frontend_blueprint)


    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('frontend.login'))
