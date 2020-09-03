from flask import Flask, render_template, url_for, flash, redirect
from .assets.forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

database_name = 'test'
#create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'NeedToCreateEnvVariableForThis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+database_name+'.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from .models.user import User
from .models.event import Event
from .models.participant import Participant
from .models.access import Access

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