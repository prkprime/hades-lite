from flask import render_template, url_for, flash, redirect

from hades.assets.forms import RegistrationForm, LoginForm
from hades.models.user import User
from hades.models.event import Event
from hades.models.participant import Participant
from hades.models.access import Access

from hades import app

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'user {form.username.data} created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'prkprime' and form.password.data == 'prkaly007':
            return redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/admin/reset_password')
def reset_password():
    return redirect(url_for('login'))