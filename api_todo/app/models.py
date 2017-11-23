# -*- coding=utf-8 -*-
from app import db
# define the database tables


# Todo table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(10))

    def __init__(self, content, state=None):
        self.content = content
        self.state = state

    def __repr__(self):
        return '<Todo %r>' % self.content
