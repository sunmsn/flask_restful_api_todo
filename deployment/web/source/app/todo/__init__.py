# -*- coding=utf-8 -*-
from flask import Blueprint

todo = Blueprint('todo', __name__)

from app.todo import routes
