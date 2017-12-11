from flask_restful import abort


def abort_unacceptable_length(attr_name):
    abort(400, message="%s is unacceptable length"%(attr_name))


def abort_username_existed(attr_name):
    abort(400, message="%s is existed"%(attr_name))


def abort_wrong_login():
    abort(400, message="wrong password or user is not existed")


def abort_role_cannot_setting():
    abort(404, message="Wrong role setting")
