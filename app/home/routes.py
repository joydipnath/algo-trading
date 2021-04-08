from app.home import blueprint
from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import logging
from app.home.forms import UpdateProfileForm
from app.base.models import User
from app import db
import app
# login_manager.blueprint_login_views = url_for('base_blueprint.login')


@blueprint.route('/dashboard')
@login_required
def index():
    return render_template('index.html', segment='index')


@blueprint.route('/profile', methods=['POST'])
@login_required
def profile():
    try:
        # update_profile_form = UpdateProfileForm(request.form)
        # if 'login' in request.form:

        # read form data
        # username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # Locate user
        user = User.query.filter_by(username=current_user.username).first()
        # print('user :' + e.encode(user))
        # Check the password
        if user:
            # user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            db.session.add(user)
            db.session.commit()
            flash("Your profile has been updated.")

    except:
        flash("We encountered some error, please try again.")
        # return None

    return redirect(url_for('home_blueprint.profile'))


@blueprint.route('/<template>', methods=['GET'])
@login_required
def route_template(template):
    try:

        form = get_forms(template)

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment, form=form )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500


# Helper - to get the form associated with a template
def get_forms(template):
    switcher = {
        'profile': UpdateProfileForm(request.form)
    }
    return switcher.get(template, "Invalid form")


# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None


# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return render_template('page-403.html'), 403
#
#
# @blueprint.errorhandler(404)
# def not_found_error(error):
#     return render_template('page-404.html'), 404
#
#
# @blueprint.errorhandler(Exception)
# def basic_error(e):
#     # fetch some info about the user from the request object
#     user_ip = request.remote_addr
#     requested_path = request.path
#
#     print("User with IP %s tried to access endpoint: %s" % (user_ip, requested_path))
#     return "An error occurred: " + str(e)