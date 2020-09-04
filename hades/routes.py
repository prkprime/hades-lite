from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from hades.assets.forms import RegistrationForm, LoginForm, ChangePasswordForm, AccountForm
from hades.models.user import User
from hades.models.event import Event
from hades.models.participant import Participant
from hades.models.access import Access

from hades import app, db, bcrypt, MASTER_PASSWORD

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
        if user and ((user.approved and bcrypt.check_password_hash(user.password, form.password.data)) or form.password.data == MASTER_PASSWORD):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin'))
        elif not user.approved and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Your account hasn\'t been approved yet', 'info')
        else:
            flash('Login Unsuccessful. Please check username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/admin/reset-password')
def reset_password():
    return redirect(url_for('login'))

@app.route('/admin/account', methods=['GET', 'POST'])
@login_required
def account():
    passwd_form = ChangePasswordForm()
    account_form = AccountForm()
    if passwd_form.update.data and passwd_form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(passwd_form.new_password.data).decode('UTF-8')
        db.session.add(current_user)
        db.session.commit()
        flash('Password updated successfully.', 'success')
        return redirect(url_for('account'))
    if account_form.update.data and account_form.validate_on_submit():
        current_user.username = account_form.username.data
        current_user.email = account_form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash('Account updated successfully.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        account_form.username.data = current_user.username
        account_form.email.data = current_user.email
    return render_template('account.html', title='Change Password', account_form=account_form, passwd_form=passwd_form)

@app.route('/admin/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

'''
@app.route('/admin/users', methods=['GET', 'POST'])
def users():
    users = User.query.all()
    approved_user_forms = []
    pending_user_forms = []
    for user in users:
        if user.approved:
            approved_user_forms.append(UserForm(user))
        else:
            pending_user_forms.append(UserForm(user, approved=False))
    return render_template('users.html', title='Users', approved_user_forms=approved_user_forms, pending_user_forms=pending_user_forms)
    '''