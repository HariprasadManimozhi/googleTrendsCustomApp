# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,DateField
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])

# pyTrends Input form
class pyTrendsForm(FlaskForm):
    keyword1 = TextField    ('Keyword 1', id='keyword1'   , validators=[DataRequired()])
    keyword2 = TextField    ('Keyword 2', id='keyword2'   , validators=[DataRequired()])
    keyword3 = TextField    ('Keyword 3', id='keyword3'   , validators=[DataRequired()])
    keyword4 = TextField    ('Keyword 4', id='keyword4'   , validators=[DataRequired()])
    keyword5 = TextField    ('Keyword 5', id='keyword5'   , validators=[DataRequired()])
