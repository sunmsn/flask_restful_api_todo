# -*- coding=utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # register the blueprint
    # from app.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/api/v1.0/auth')

    from app.todo import todo as todo_blueprint
    app.register_blueprint(todo_blueprint, url_prefix='/api/v1.0/todo')


    return app
