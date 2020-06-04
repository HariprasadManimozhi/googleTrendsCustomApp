# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from flask import flash

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm,pyTrendsForm
from app.base.models import User

from app.base.util import verify_pass

# Py trends
from pytrends.request import TrendReq

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', msg='Username already registered', form=create_account_form)

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', msg='Email already registered', form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', msg='User created please <a href="/login">login</a>', form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@blueprint.route('/pytrends1', methods=['GET', 'POST'])
def trends_chart():
    # get user input from form
    pytrends_form = pyTrendsForm(request.form)

    # if data input from form
    if request.method == 'POST':

        keyword1 = request.form.get('keyword1',False)
        keyword2 = request.form.get('keyword2',False)
        keyword3 = request.form.get('keyword3',False)
        keyword4 = request.form.get('keyword4',False)
        keyword5 = request.form.get('keyword5',False)
        #Category = request.form.get('Category',False)
        #FromDate = request.form.get('FromDate',False)
        #ToDate = request.form.get('ToDate',False)

        #keyword1 = request.form['keyword1']
        #keyword2 = request.form['keyword2']
        #keyword3 = request.form['keyword3']
        #keyword4 = request.form['keyword4']
        #keyword5 = request.form['keyword5']
        #Category = request.form['Category']
        #FromDate = request.form['fromDate']
        #ToDate = request.form['toDate']

        print(keyword1, "vs", keyword2, "vs", keyword3,"vs", keyword4,"vs", keyword5)

        if pytrends_form.validate():
            #Save the comment here.
            flash('Analyzing ' + keyword1 + ' vs ' + keyword2 + ' vs ' + keyword3 + ' vs ' + keyword4 + ' vs ' + keyword5 )
        else:
            flash('Error: All the form fields are required.')
            return render_template("errors/500.html", form=pytrends_form)

    elif request.method == 'GET':
    # default for when GET first runs we have no input
        keyword1 = 'first'
        keyword2 = 'second'
        keyword3 = 'third'
        keyword4 = 'fourth'
        keyword5 = 'fifth'
        #Category = 'Category'
        #FromDate = 'FromDate'
        #ToDate = 'ToDate'

    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq()

    # get google trends data past 24 hours
    pytrend.build_payload(kw_list=[keyword1,keyword2,keyword3,keyword4,keyword5],cat=71 ,timeframe='today 12-m', geo='IN')
    food_24h_df = pytrend.interest_over_time()

    # time - y axis
    time_24h = food_24h_df.index
    # interest values - x axis
    food1_24h = food_24h_df[keyword1]
    food2_24h = food_24h_df[keyword2]
    food3_24h = food_24h_df[keyword3]
    food4_24h = food_24h_df[keyword4]
    food5_24h = food_24h_df[keyword5]

    # get google trends data past week
    pytrend.build_payload(kw_list=[keyword1, keyword2,keyword3,keyword4,keyword5],cat=71, timeframe='today 3-m', geo='IN')
    food_7d_df = pytrend.interest_over_time()

    # time - y axis
    time_7d = food_7d_df.index
    # interest values - x axis
    food1_7d = food_7d_df[keyword1]
    food2_7d = food_7d_df[keyword2]
    food3_7d = food_7d_df[keyword3]
    food4_7d = food_7d_df[keyword4]
    food5_7d = food_7d_df[keyword5]

    return render_template("forms_ff.html", form=pytrends_form,
                    keyword1=keyword1, keyword2=keyword2,keyword3=keyword3,keyword4=keyword4,keyword5=keyword5,
                    time_24h=time_24h, time_7d=time_7d,
                    food1_24h=food1_24h, food2_24h=food2_24h,food3_24h=food3_24h,food4_24h=food4_24h,food5_24h=food5_24h,
                    food1_7d=food1_7d, food2_7d=food2_7d,food3_7d=food3_7d,food4_7d=food4_7d,food5_7d=food5_7d
                    )
