from flask import Blueprint, render_template, redirect, request, url_for, abort, flash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegistrationForm
from ..db import db

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/')
def home():
    return render_template('home.html')


@auth_bp.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('auth.home'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash("Logged in Successfully!")

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('auth.welcome_user')

            return redirect(next)

    return render_template('login.html', form=form)



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(form.email.data,
                    form.username.data,
                    form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Thanks for registration!")
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/list')
def list():
    users = User.query.all()
    return render_template('list.html', users=users)
