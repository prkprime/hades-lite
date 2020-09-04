from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from hades.assets.forms import RegistrationForm, LoginForm, ChangePasswordForm, AccountForm, PendingUserForm, ApprovedUserForm
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
    if request.method == 'POST':
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
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.approved and bcrypt.check_password_hash(user.password, form.password.data):
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
    return render_template('account.html', title='Account', account_form=account_form, passwd_form=passwd_form)

@app.route('/admin/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    approved_user_forms = {}
    pending_user_forms = {}
    for user in users:
        if user.approved:
            form = ApprovedUserForm(id=user.id)
            form.username.data = user.username
            form.email.data = user.email
            approved_user_forms[user.id] = form
        else:
            form = PendingUserForm(id=user.id)
            form.username.data = user.username
            form.email.data = user.email
            pending_user_forms[user.id] = form
    if request.method == 'POST':
        if request.form.get('approve'):
            return redirect(url_for('manage_user', action='approve', id=request.form.get('id')))
        elif request.form.get('reject'):
            return redirect(url_for('manage_user', action='reject', id=request.form.get('id')))
        elif request.form.get('delete'):
            return redirect(url_for('manage_user', action='delete', id=request.form.get('id')))
    return render_template('users.html', title='Users', approved_user_forms=approved_user_forms, pending_user_forms=pending_user_forms)

@app.route('/admin/users/<action>/<id>')
@login_required
def manage_user(action, id):
    if action == 'approve':
        user = User.query.filter_by(id=id).first()
        user.approved = True
        db.session.add(user)
        db.session.commit()
        flash(f'Approved user \'{user.username}\' successfully', 'success')
    elif action == 'reject' or action == 'delete':
        print('1')
        username = User.query.filter_by(id=id).first().username
        db.session.query(User).filter_by(id=id).delete()
        db.session.commit()
        if action == 'reject':
            flash(f'Rejected user \'{username}\' successfully', 'success')
        else:
            print('1')
            flash(f'Deleted user \'{username}\' successfully', 'success')
    return redirect(url_for('users'))