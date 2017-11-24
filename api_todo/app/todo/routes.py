# -*- coding=utf-8 -*-
from flask_restful import Api, fields, Resource
from flask_restful import marshal_with, reqparse

from app.todo import todo
from app.models import Todo
from app.todo.errors import *
from app import db

# flask-restful 设置
api = Api(todo)
# 返回json序列化
todo_fields = {
    "id": fields.Integer,
    "content": fields.String,
    "state": fields.String
}

# To do list API
class TodoList(Resource):
    """
    Get one list of todo tasks, or create a list of todo tasks
    """
    @marshal_with(todo_fields, envelope='todo')
    def get(self):
        todo = Todo.query.all()
        return todo

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', required=True)
        parser.add_argument('state')
        args = parser.parse_args()
        # 验证长度
        if len(args['content']) ==0 or len(args['content']) > 25:
            abort_unacceptable_length("content")
        if args['state'] is not None:
            if len(args['state']) > 10:
                abort_unacceptable_length("state")
        # 写入数据库
        new_todo = Todo(content=args['content'],
                        state=args['state'])
        db.session.add(new_todo)
        db.session.commit()
        return "insert: %s"%(args['content']), 201

# To do detail API
class TodoDetail(Resource):
    """
    operate (delete,search,update) one todo task
    """
    def get_object(self, id):
        todo = Todo.query.filter_by(id=id).first()
        if not todo:
            abort_id_cannot_found()
        return todo

    @marshal_with(todo_fields)
    def get(self, id):
        todo = self.get_object(id)
        return todo

    def delete(self, id):
        todo = self.get_object(id)
        db.session.delete(todo)
        db.session.commit()
        return 'delete todo ' + id, 204

    @marshal_with(todo_fields)
    def put(self, id):
        todo = self.get_object(id)
        # 获取参数
        parser = reqparse.RequestParser()
        parser.add_argument('content')
        parser.add_argument('state')
        args = parser.parse_args()
        # 验证长度
        if args['content'] is not None:
            if len(args['content']) ==0 or len(args['content']) > 25:
                abort_unacceptable_length("content")
        if args['state'] is not None:
            if len(args['state']) > 10:
                abort_unacceptable_length("state")
        # 修改数据
        if args['content']:
            todo.content = args['content']
        if args['state']:
            todo.state = args['state']
        db.session.commit()
        return todo, 201


# 配置路由
api.add_resource(TodoList, '')
api.add_resource(TodoDetail, '/<id>')
