from flask import Flask, url_for, redirect, request, flash
from flask_login import LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
import logging
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from flask.json import JSONEncoder
from datetime import datetime


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('base', 'home', 'admin', 'errors'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def register_logging(app):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    # log.addHandler(handler)
    # current date and time
    now = datetime.now()
    # date and time format: dd/mm/YYYY H:M:S
    format = "%d-%m-%Y"
    filename = 'logs/'+now.strftime(format)+'-flask.log'
    basicConfig(filename=filename, level=DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')



def request_func(app):

    """
    This function will run before every request. Let's add something to the session & g.
    It's a good place for things like establishing database connections, retrieving
    user information from the session, assigning values to the flask g object etc..
    We have access to the request context.
    """

    @app.before_request
    def before_request():
        if not current_user.is_authenticated and request.path != '/login':
            logout_user()
            # return request.endpoint
            flash("We have logged you out, just to be safe.")
            return redirect('/login')


def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    register_logging(app)
    request_func(app)
    # login_manager.blueprint_login_views = url_for('base_blueprint.login')
    # login_manager.blueprint_login_views =  {
    #     'base': url_for('base_blueprint.login'),
        # 'customers': '/customer/login',
        # 'admin' : '/admin/login',
    # }

    return app