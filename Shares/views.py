#! /usr/bin/env python
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from Shares import app, db, login_manager
from forms import *
from models import User, Userownedshare, Share
from share_data import *
import json


@login_manager.user_loader
def load_user(userid):

    if userid is None or userid == 'None':
       userid =0
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():

    if current_user.is_authenticated:

        share_data.getportfoliovalues(current_user.username)

        return render_template('index.html', shares=share_data.getalljsonshares(current_user.username), portfolioids=share_data.getportfolioidsfromtable(current_user.username))

    else: return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data.lower(),
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('index'))

        flash('Incorrect username or password.')
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/editportfolios', methods=['GET', 'POST'], )
@login_required
def editportfolios():

    form = AddPortfolioForm()
    d_form = DeletePortfolioForm()
    d_form.name.choices = [(h, h) for h in share_data.getportfolioidsfromtable(current_user.username)]

    if form.validate_on_submit():
        name = form.name.data

        portfolio = Portfolios(portfolioname=name.lower(), username=current_user.username)
        db.session.add(portfolio)
        db.session.commit()

        flash("Added portfolio '{}'".format(name))
        return redirect(url_for('index'))


    if d_form.validate_on_submit():
        name = d_form.name.data

        portfolio = share_data.getPortfolioIDbyusernameandPortfolioName(current_user.username, name)
        db.session.delete(portfolio)
        db.session.commit()

        flash("deleted portfolio '{}'".format(name))
        return redirect(url_for('index'))


    return render_template('editportfolios.html', form=form, d_form=d_form, portfolioids=share_data.getportfolioidsfromtable(current_user.username) )


@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_share(bookmark_id):
    tempeditshare = Userownedshare.query.get_or_404(bookmark_id)
    if current_user.username != tempeditshare.user:
        abort(403)
    form = EditShareForm(obj=tempeditshare)
    form.portfolioid.choices = [(h, h) for h in share_data.getportfolioidsfromtable(current_user.username)]
    form.originalportfolioid.data = Userownedshare.query.get_or_404(bookmark_id).portfolioid

    if form.validate_on_submit():
        form.populate_obj(tempeditshare)
        db.session.commit()
        flash("You have successfully edited the share: '{}'". format(tempeditshare.name.name))
        return redirect(url_for('index'))

    return render_template('editshare_form.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username), form=form, title="Edit share")


@app.route('/delete/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def delete_share(bookmark_id):
    tempshare = Userownedshare.query.get_or_404(bookmark_id)
    if current_user.username != tempshare.user:
        abort(403)

    if request.method == "POST":
        db.session.delete(tempshare)
        db.session.commit()
        flash("You have successfully deleted the share: '{}'". format(tempshare.name.name))
        return redirect(url_for('index'))
    else:
        flash("Please confirm deleting the bookmark.")

    return render_template('confirm_deletes_share.html', portfolioids=Userownedshare.listportfolios(), share=tempshare, nolinks=True)


@app.route('/portfolio/<string:portfolio_id>', methods=['GET', 'POST'])
@login_required
def list_portfolio(portfolio_id):

    allshares = share_data.getalljsonshares(current_user.username)
    sharesinportfolio = []

    for share in allshares:

        if share['portfolioid'] == portfolio_id:

            sharesinportfolio.append(share)


    return render_template('portfolio.html', id=portfolio_id, portfolioids = share_data.getportfolioidsfromtable(current_user.username), portfolioshares=sharesinportfolio, portfoliovalue=share_data.getsubportfoliovalue(current_user.username, portfolio_id ))


@app.route('/add', methods=['GET', 'POST'], )
@login_required
def add():
    form = AddShareForm()
    form.portfolioid.choices = [(h, h) for h in share_data.getportfolioidsfromtable(current_user.username)]
    if form.validate_on_submit():
        ticker = form.ticker.data.upper()
        quantity = form.quantity.data
        dividends = form.dividends.data
        portfolioid = form.portfolioid.data


        if not Share.exists(ticker):

            sharedata = share_data.JSONSharePrice(ticker)
            sharename = sharedata['query']['results']['quote']['Name']

            newshare = Share(ticker=ticker, name=sharename)
            db.session.add(newshare)
           # db.session.commit()

        bm = Userownedshare(user=current_user.username, quantity=quantity, ticker=ticker, dividends=dividends, portfolioid=portfolioid)
        db.session.add(bm)
        db.session.commit()
        flash("Added share '{}'".format(ticker))
        return redirect(url_for('index'))
    return render_template('add.html', form=form, portfolioids=share_data.getportfolioidsfromtable(current_user.username), )


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

    if current_user.is_authenticated:

        return render_template('sharedata.html', data=share_data.getalljsonshares(current_user.username),
                                portfoliovalues= share_data.getportfoliovalues(current_user.username))

















