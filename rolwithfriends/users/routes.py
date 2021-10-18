from flask import Blueprint, render_template, url_for, flash, redirect, request
from rolwithfriends.users.forms import (LoginForm, RegistrationForm, UpdateAccountForm, 
                                  RequestResetForm, ResetPasswordForm)
from rolwithfriends.models import User
from rolwithfriends import mongo, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from bson.objectid import ObjectId
from flask_mail import Message

from rolwithfriends.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    login = LoginForm()
    if login.validate_on_submit():
        user = mongo.db.User.find_one({"email": login.email.data})
        if user and bcrypt.check_password_hash(user['password'], login.password.data):
            logUser = User(user)
            login_user(logUser, remember=login.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash('Login unsuccesful. Please check username and password.', 'danger')
    
    return render_template('login.html', title="Login", form=login)

@users.route("/signup", methods=['GET', 'POST'])
def signup():
    signup = RegistrationForm()
    if signup.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(signup.password.data).decode('utf-8')
        newUser = mongo.db.User.insert_one({"role": "user","username": signup.username.data, "email": signup.email.data, 
                                            "password": hashed_password, 
                                            "image_file": "https://res.cloudinary.com/zoopast/image/upload/v1634530345/RolWithFriends/profile_pics/default.png", 
                                            "gamesIn": [], "characters": [],
                                            "gamesOwner": []})
        flash(f'Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('signup.html', title="Signup", form=signup)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    update = UpdateAccountForm()
    if update.validate_on_submit():

        if update.picture.data:
            picture_file = save_picture(update.picture.data)
            user = mongo.db.User.update_one({"_id": ObjectId(current_user.id)},{"$set":{"image_file": picture_file}})
        user = mongo.db.User.update_one({"_id": ObjectId(current_user.id)},{"$set":{"username": update.username.data, "email": update.email.data}})
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        update.username.data = current_user.username
        update.email.data = current_user.email
    image_file = current_user.image_file
    return render_template('account.html', title="Account", 
                            image_file = image_file, form = update)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        find_user = mongo.db.User.find_one({"email": form.email.data})
        if find_user:
            user = User(find_user)
            send_reset_email(user)
        flash('If an account with this email address exists, a password reset message will be sent shortly','info')
        return redirect(url_for('main.home'))
    return render_template('reset_request.html', title="Reset password", form = form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Thats is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            mongo.db.User.update_one({"_id": user.id},{"$set":{"password": hashed_password}})
            flash(f'Your password has been updated! You are now able to log in!', 'success')
            return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset password", form = form)