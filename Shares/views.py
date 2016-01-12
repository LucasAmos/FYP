#! /usr/bin/env python
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from Shares import app, db, login_manager
from forms import ShareForm, LoginForm, SignupForm, EditShareForm
from models import User, Userownedshare
from share_data import share_data
import json
from sets import Set

@login_manager.user_loader
def load_user(userid):

    if userid is None or userid == 'None':
       userid =0
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():

    if current_user.is_authenticated:



        return render_template('index.html', shares=share_data.getalljsonshares(current_user.username), portfolioids = Userownedshare.listportfolios())

    else: return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ShareForm()
    if form.validate_on_submit():
        ticker = form.ticker.data
        quantity = form.quantity.data
        dividends = form.dividends.data
        bm = Userownedshare(user=current_user.username, quantity=quantity, ticker=ticker, dividends=dividends)
        db.session.add(bm)
        db.session.commit()
        flash("Added share '{}'".format(ticker))
        return redirect(url_for('index'))
    return render_template('add.html', form=form, portfolioids = Userownedshare.listportfolios())


@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_share(bookmark_id):
    tempeditshare = Userownedshare.query.get_or_404(bookmark_id)
    if current_user.username != tempeditshare.user:
        abort(403)
    form = EditShareForm(obj=tempeditshare)
    if form.validate_on_submit():
        form.populate_obj(tempeditshare)
        db.session.commit()
        flash("You have successfully edited the share: '{}'". format(tempeditshare.name.name))
        return redirect(url_for('index'))

    return render_template('editshare_form.html', portfolioids = Userownedshare.listportfolios(), form=form, title="Edit share")



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('index', username=user.username))

        flash('Incorrect username or password.')
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

from StringIO import StringIO
io = StringIO()

from StringIO import StringIO


@app.route('/sharedata')
def sharedata():
    js = share_data.getalljsonshares(current_user.username)
    io = StringIO()
    #return json.dumps(js, io)
    data= json.dumps(js, io)

    if current_user.is_authenticated:

        return render_template('sharedata.html', data=share_data.getalljsonshares(current_user.username),
                               portfolioids=Userownedshare.listportfolios())


@app.route('/portfoliovalue')
def portfoliovalue():

    if current_user.is_authenticated:

        return render_template('portfoliovalue.html', data=share_data.getportfoliovalue(current_user.username))


@app.route('/portfolio/<string:portfolio_id>', methods=['GET', 'POST'])
@login_required
def list_portfolio(portfolio_id):

    allshares = share_data.getalljsonshares(current_user.username)
    sharesinportfolio = []

    for share in allshares:

        if share['portfolioid'] == portfolio_id:

            sharesinportfolio.append(share)


    return render_template('portfolio.html', id=portfolio_id, portfolioids = Userownedshare.listportfolios(), portfolioshares=sharesinportfolio)














