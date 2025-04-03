#auth routes setup
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
#define auth blueprint

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category='success')
                login_user(user, remember=True)#remember for this session
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email not found", category='error')

    return render_template("login.html", user=current_user)
    #you can return variables in the params of the render template
    #example render_template("login.html", text="text")
    #flask configures jinja2 template engine automatically
    #you can go into the login.html file and write {{text}} to access this variable
    #and you can write expressions with it, {{ if text == "text" }}

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category='error')
        elif len(first_name) < 2:
            flash("First name must have more than 1 character", category='error')
        elif password1 != password2:
            flash("Passwords don't match!", category='error')
        elif len(password1) < 7:
            flash("Password needs to be more than 6 characters", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created.", category='success')
            login_user(new_user, remember=True)  # remember for this session
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)