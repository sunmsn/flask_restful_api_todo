# -*- coding=utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

class Config:
    SECRET_KEY = 'this_is_todo_api_key' # input the secret key
    SECURITY_PASSWORD_SALT = 'this_is_salt_for_todo_api_key'

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # gmail authentication
    MAIL_USERNAME = 'flask.restful.api.todo@gmail.com'
    MAIL_PASSWORD = 'flask_restful_api_todo'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'flask.restful.api.todo@gmail.com'

    # sqlalchemy 设置
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 生成 back.log 日志
    @staticmethod
    def init_app(app):
        handler = RotatingFileHandler('back.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)

# the config for development
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://todo:todo@localhost/todo?charset=utf8'
    DEBUG = True

class DeploymentConfig(Config):
    DEBUG = False

# define the config
config = {
    'development': DevelopmentConfig,
    'deployment': DeploymentConfig
}
