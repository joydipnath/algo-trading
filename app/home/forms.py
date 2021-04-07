from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, FileField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo
from wtforms import ValidationError, validators
from flask_login import login_required, current_user
import math
import re
import uuid
import warnings


def input_max_length(form, field):
    if len(field.data) > 50:
        raise ValidationError('Field must be less than 50 characters')


## Profile
class UpdateProfileForm(FlaskForm):
    username = TextField('Username', id='username', default=current_user, validators=[DataRequired(), validators.length(min=1, max=30)])
    first_name = TextField('First Name', id='first_name', default=current_user, validators=[validators.optional(), validators.length(min=1, max=30)])
    last_name = TextField('Last Name', id='last_name', validators=[validators.optional(), validators.length(min=1, max=30, message="maximum 30 char is allowed.")])
    # password = PasswordField('Password', id='password', validators=[validators.optional(), validators.length(min=6, max=15)])
    # confirm_password = PasswordField('Confirm Password', id='confirm_password', validators=[validators.optional(), EqualTo('password', message='Passwords must match')])
    email = TextField('Email', id='email', validators=[DataRequired(), Email(), input_max_length])
    # image = FileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])
    submit = SubmitField(label=('Update Profile'))