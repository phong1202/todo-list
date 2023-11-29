from flask import render_template, redirect, flash, Blueprint, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.todo import User
from app.extensions import db
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse

bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=16)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=16)])
    password_confirmation = PasswordField('Re-enter password', validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email has already been used!')

# Signup route
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # Already loginned
    if current_user.is_authenticated:
        return redirect(url_for('main.to_do'))
    
    # Form validation
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        password_confirmation = form.password_confirmation.data
        if password_confirmation != password:
            flash('Password confirmation is not the same as password field!', 'error')
            return redirect(url_for('auth.signup'))
        user = User(email=email, username=username)
        user.set_password(password)
        if User.query.filter_by(username=username).first() is not None:
            flash('This username has already been signed up!', 'error')
            return redirect(url_for('auth.signup'))
        # elif User.query.filter_by(email=email).first() is not None:
        #     flash('This email has already been used!', 'error')
        #     return redirect(url_for('auth.signup'))
        else:
            db.session.add(user)
            db.session.commit()
            flash('Sign up successfully!', 'success')
            return(redirect(url_for('auth.login')))
    return render_template('signup.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Already loginned
    if current_user.is_authenticated:
        return redirect(url_for('main.to_do'))
    
    # Form validation
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.check_password(form.password.data) is False:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page =  request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.to_do')
        flash('Login successful!', 'success')
        return redirect(next_page)
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out!', 'info')
    return redirect(url_for('auth.login'))