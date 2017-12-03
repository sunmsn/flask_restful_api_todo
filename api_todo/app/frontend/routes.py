# -*- coding=utf-8 -*-
from flask import render_template
from flask_login import login_required, logout_user

from app.frontend import frontend


@frontend.route('/')
@login_required
def main():
    return render_template('main.html')


@frontend.route('/register')
def register():
    return render_template('auth/register.html')


@frontend.route('/register_finished')
def register_finished():
    return render_template('auth/register_finished.html')


@frontend.route('/confirm/<token>')
def confirm_email(token):
    return render_template('auth/confirm_email.html')


@frontend.route('/login')
def login():
    return render_template('auth/login.html')


@frontend.route("/logout")
@login_required
def logout():
    logout_user()
    return "redirect(somewhere)"
