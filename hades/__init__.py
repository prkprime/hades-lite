from flask import Flask, render_template, url_for, flash, redirect
from hades.assets.forms import RegistrationForm, LoginForm

#create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'NeedToCreateEnvVariableForThis'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'user {form.username.data} created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'prkprime' and form.password.data == 'prkaly007':
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/reset_password')
def reset_password():
    return redirect(url_for('login'))