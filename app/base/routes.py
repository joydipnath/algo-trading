from flask import jsonify, render_template, redirect, request, url_for, session, flash, current_app
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
import logging
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User
from app.base.util import verify_pass
import json


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login') + '?next=' + request.path)


## Login & Registration
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        # Locate user
        user = User.query.filter_by(username=username).first()
        e = json.JSONEncoder()
        # print('user :' + e.encode(user))
        # Check the password
        if user and verify_pass( password, user.password):
            session.permanent = True
            login_user(user, remember=remember)
            current_app.logger.info('User login:' + current_user.username)
            flash("You have logged you in.")
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect('/')

    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html',
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/login">login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout', methods=["GET"])
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for('base_blueprint.login'))


## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404


# @blueprint.errorhandler(401)
# def not_found_error(error):
#     return render_template('page-404.html'), 401


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-404.html'), 500