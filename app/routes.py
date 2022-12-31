# -*- coding: utf-8 -*-

from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title = "Home", user = current_user)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Incorrect username or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc == "":
            return redirect(url_for("index"))
        return redirect(next_page)

    return render_template("login.html", title = "Sign in", form = form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been successful logout!")
    return redirect(url_for("index"))