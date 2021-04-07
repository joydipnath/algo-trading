'''Application error handlers.'''

from app.errors import blueprint
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import logging


# from app.models.threatstack import ThreatStackError


# @blueprint.app_errorhandler(ThreatStackError)
# def handle_error(error):
#     message = [str(x) for x in error.args]
#     status_code = 500
#     success = False
#     response = {
#         'success': success,
#         'error': {
#             'type': error.__class__.__name__,
#             'message': message
#         }
#     }
#
#     return jsonify(response), status_code


@blueprint.app_errorhandler(Exception)
def handle_unexpected_error(error):
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            # 'type': 'UnexpectedException',
            'type': error.__class__.__name__,
            'message': 'An unexpected error has occurred.',
            'error': str(error)
        }
    }

    return jsonify(response), status_code


@blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404