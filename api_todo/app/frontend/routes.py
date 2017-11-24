# -*- coding=utf-8 -*-
from flask import render_template

from app.frontend import frontend


@frontend.route('/')
def main():
    return render_template('main.html')
