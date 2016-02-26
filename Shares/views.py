#! /usr/bin/env python
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from Shares import app, db, login_manager
from forms import *
from models import User, Share
from share_data import *
from temp import *

@login_manager.user_loader
def load_user(userid):

    if userid is None or userid == 'None':
        userid =0
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:

        try:


            #print temp.getTickers("lucas")



            return render_template('index.html', shares=share_data.getalljsonshares(current_user.username),
                                   portfolioids=share_data.getportfolioidsfromtable(current_user.username))

        except:
            return render_template("connectiondown.html")

    else: return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data.lower(),
                    password=form.password.data,
                    phonenumber=form.phonenumber.data,
                    emailfrequency=0,
                    smsenabled=False)
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


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/addportfolio', methods=['GET', 'POST'] )
@login_required
def addportfolio():

    form = AddPortfolioForm()

    if form.validate_on_submit():
        name = form.name.data.lower()

        portfolio = Portfolios(portfolioname=name.lower(), username=current_user.username)
        db.session.add(portfolio)
        db.session.commit()

        flash("Added portfolio '{}'".format(name))
        return redirect(url_for('index'))

    return render_template('addportfolio.html', form=form, portfolioids=share_data.getportfolioidsfromtable(current_user.username))


@app.route('/deleteportfolio', methods=['GET', 'POST'])
@login_required
def deleteportfolio():

    d_form = DeletePortfolioForm()
    d_form.name.choices = [(h, h) for h in share_data.getportfolioidsfromtable(current_user.username)]


    if d_form.validate_on_submit():
        name2 = d_form.name.data

        portfolio = share_data.getPortfolioIDbyusernameandPortfolioName(current_user.username, name2)
        db.session.delete(portfolio)
        db.session.commit()

        flash("deleted portfolio '{}'".format(name2))
        return redirect(url_for('index'))

    return render_template('deleteportfolio.html', d_form=d_form, portfolioids=share_data.getportfolioidsfromtable(current_user.username))


@app.route('/delete/<share_id>', methods=['GET', 'POST'])
@login_required
def delete_share(share_id):
    tempshare = Userownedshare.query.get_or_404(share_id)
    if current_user.username != tempshare.user:
        abort(403)

    if request.method == "POST":
        db.session.delete(tempshare)
        db.session.commit()
        flash("You have successfully deleted the share: '{}'". format(tempshare.name.name))
        return redirect(url_for('list_portfolio', portfolio_id=tempshare.portfolioid))
    else:
        flash("Please confirm deleting the share.")

    return render_template('confirm_deletes_share.html', portfolioids=Userownedshare.listportfolios(current_user.username), share=tempshare, nolinks=True)


@app.route('/portfolio/<string:portfolio_id>', methods=['GET', 'POST'])
@login_required
def list_portfolio(portfolio_id):

    try:

        allshares = share_data.getalljsonshares(current_user.username)
        sharesinportfolio = []
        profit = 0

        for share in allshares:

            if share['portfolioid'] == portfolio_id:

                share['profit'] =(float(share['price']) * share['quantity']) - (share['averagepurchaseprice'] * share['quantity'])
                sharesinportfolio.append(share)
                profit += share['profit']


        return render_template('portfolio.html', id=portfolio_id, portfolioids = share_data.getportfolioidsfromtable(current_user.username),
                               portfolioshares=sharesinportfolio, portfoliovalue=share_data.getsubportfoliovalue(current_user.username, portfolio_id),
                               portfolioprofit=profit)

    except:
            return render_template("connectiondown.html")


@app.route('/add', methods=['GET', 'POST'], )
@login_required
def add():
    form = AddShareForm()
    form.portfolioid.choices = [(h, h) for h in share_data.getportfolioidsfromtable(current_user.username)]
    if form.validate_on_submit():
        ticker = form.ticker.data.upper()
        quantity = form.quantity.data
        dividends = form.dividends.data
        purchaseprice = form.purchaseprice.data
        portfolioid = form.portfolioid.data


        if not Share.exists(ticker):

            sharedata = share_data.JSONSharePrice(ticker)
            sharename = sharedata['query']['results']['quote']['Name']

            newshare = Share(ticker=ticker, name=sharename)
            db.session.add(newshare)

        share = Userownedshare(user=current_user.username, quantity=quantity, ticker=ticker, dividends=dividends, averagepurchaseprice=purchaseprice, portfolioid=portfolioid)
        db.session.add(share)
        db.session.commit()
        flash("Added share '{}'".format(ticker))
        return redirect(url_for('index'))
    return render_template('add.html', form=form, portfolioids=share_data.getportfolioidsfromtable(current_user.username))


@app.route('/addadditionalshares/<string:share_id>', methods=['GET', 'POST'], )
@login_required
def addadditionalshares(share_id):
    share = Userownedshare.query.get_or_404(share_id)

    if current_user.username != share.user:
        abort(403)
    form = AddAdditionalShares()

    if form.validate_on_submit():

        if form.sharequantity.data and form.shareprice.data:

            totalshares = float(share.quantity) + form.sharequantity.data
            newaveragepurchaseprice = (((float(share.averagepurchaseprice) * share.quantity) + (form.sharequantity.data * form.shareprice.data)) / totalshares)
            share.averagepurchaseprice = newaveragepurchaseprice

            share.quantity += form.sharequantity.data
            db.session.commit()

        if form.dividends.data:
            share.dividends += float(form.dividends.data)
            db.session.commit()

        flash("You have successfully edited the share: '{}'". format(share.name.name))
        return redirect(url_for('list_portfolio', portfolio_id=share.portfolioid))

    return render_template('addadditionalshares.html', form=form, portfolioids=share_data.getportfolioidsfromtable(current_user.username), name=share.name.name)


@app.route('/sell/<share_id>', methods=['GET', 'POST'])
@login_required
def sell_share(share_id):
    share = Userownedshare.query.get_or_404(share_id)
    if current_user.username != share.user:
        abort(403)
    form = RemoveShareForm()
    form.ticker.data = share.ticker

    form.originalportfolioid.data = Userownedshare.query.get_or_404(share_id).portfolioid
    form.shareID.data=share_id

    if form.validate_on_submit():

        originalpurchaseprice = float(share.averagepurchaseprice)
        originalquantity = float(share.quantity)
        salequantity = float(form.quantity.data)
        saleprice = float(form.price.data)



        if (originalquantity - salequantity) == 0:

            newpurchaseprice = 0

        else:
            newpurchaseprice = str(((originalpurchaseprice * originalquantity) - (saleprice * salequantity)) /
                               (originalquantity-salequantity)
        )

        share.averagepurchaseprice = newpurchaseprice
        share.quantity = (originalquantity - salequantity)
        db.session.commit()

        db.session.commit()

        flash("You have successfully edited the share: '{}'". format(share.name.name))
        return redirect(url_for('list_portfolio', portfolio_id=share.portfolioid))

    return render_template('sellshare_form.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username), form=form)


@app.route('/notifications', methods=['GET', 'POST'], )
@login_required
def notifications():
    user = User.query.get_or_404(current_user.id)
    form = NotificationSettingsForm()

    if form.validate_on_submit():
        user.emailfrequency = form.emailfrequency.data
        user.smsenabled = form.smsenabled.data

        db.session.commit()
        flash("You have successfully updated your notification preferences")
        return redirect(url_for('index'))



    return render_template('notifications.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username), form=form)

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


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

        allshares = share_data.getalljsonshares(current_user.username)
        sharesinportfolio = []

        for share in allshares:
                share['profit'] =(float(share['price']) * share['quantity']) - (share['averagepurchaseprice'] * share['quantity'])
                sharesinportfolio.append(share)

        profits ={}
        for share in sharesinportfolio:

            if share['portfolioid'] in profits:

                profits[share['portfolioid']] = profits[share['portfolioid']] + share['profit']

            else:
                profits[share['portfolioid']] = share['profit']

        return render_template('sharedata.html', data=sharesinportfolio,
                               portfoliovalues=share_data.getportfoliovalues(current_user.username), portfolioprofits=profits,
                               ids=share_data.getportfolioidsfromtable(current_user.username))

















