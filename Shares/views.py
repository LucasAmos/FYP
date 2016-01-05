#! /usr/bin/env python
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from Shares import app, db, login_manager
from forms import BookmarkForm, LoginForm, SignupForm
from models import User, Userownedshare
#from share_data import getalljsonshares
from share_data import share_data


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():

    if current_user.is_authenticated:
        print(share_data.getalljsonshares(current_user.username))

    return render_template('index.html', shares=share_data.getalljsonshares(current_user.username))
    #return render_template('index.html', shares=Userownedshare.listshares())


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        ticker = form.ticker.data
        quantity = form.quantity.data
        bm = Userownedshare(user=current_user.username, quantity=quantity, ticker=ticker)
        db.session.add(bm)
        db.session.commit()
        flash("Added share '{}'".format(ticker))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


# @app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
# @login_required
# def edit_bookmark(bookmark_id):
#     bookmark = Bookmark.query.get_or_404(bookmark_id)
#     if current_user != bookmark.user:
#         abort(403)
#     form = BookmarkForm(obj=bookmark)
#     if form.validate_on_submit():
#         form.populate_obj(bookmark)
#         db.session.commit()
#         flash("Stored '{}'". format(bookmark.description))
#         return redirect(url_for('user', username=current_user.username))
#     return render_template('bookmark_form.html', form=form, title="Edit bookmark")




@app.route('/user/<username>')
def user(username):
    # user = User.query.filter_by(username=username).first_or_404()
    # print(current_user.username)
    # print "test"
    #
    # if current_user.username == user.username:
    #     return render_template('user.html', user=user)
    # else:
        return render_template('404.html')

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





