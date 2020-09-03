from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from hades.assets.forms import RegistrationForm, LoginForm
from hades.models.user import User
from hades.models.event import Event
from hades.models.participant import Participant
from hades.models.access import Access

from hades import app, db, bcrypt

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_passwd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_passwd)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin'))
        flash('Login Unsuccessful. Please check username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/admin/reset_password')
def reset_password():
    return redirect(url_for('login'))

@app.route('/admin/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))