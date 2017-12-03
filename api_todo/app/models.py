# -*- coding=utf-8 -*-
from app import db
import datetime
from passlib.apps import custom_app_context as pwd_context
# define the database tables

##################################
# User data ######################
##################################
# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    is_authenticated = db.Column(db.Boolean)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.id

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.is_authenticated

    def get_id(self):
        """Return the id"""
        return self.id

# LocalAuth table
class LocalAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User",
                           backref=db.backref('local_auth', lazy='dynamic'))


    def __init__(self, user, username=None,
                 password_hash=None, email=None,
                 registered_on=None, confirmed=None):
        self.user = user
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.registered_on = registered_on
        self.confirmed = confirmed

    def __repr__(self):
        return '<LocalAuth %r>' % self.id

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

# OAuth table
class OAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oauth_name = db.Column(db.String(32), unique=True)
    oauth_id = db.Column(db.String(32))
    oauth_access_token = db.Column(db.String(128))
    oauth_expires = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User",
                           backref=db.backref('o_auth', lazy='dynamic'))


##################################
# Bussiness data #################
##################################
# Todo table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(10))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User",
                           backref=db.backref('todo', lazy='dynamic'))

    def __init__(self, content, state=None):
        self.content = content
        self.state = state

    def __repr__(self):
        return '<Todo %r>' % self.content
