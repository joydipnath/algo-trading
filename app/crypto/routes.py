from app.crypto import blueprint
from flask import render_template, redirect, url_for, request, flash, current_app, abort
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound


@blueprint.route('home', methods=['GET'])
@login_required
def index():
    try:
        return render_template('crypto_dashboard.html', segment='crypto')
    except TemplateNotFound:
        abort(404)