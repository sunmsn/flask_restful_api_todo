# -*- coding=utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

class Config:
    SECRET_KEY = '' # input the secret key

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
