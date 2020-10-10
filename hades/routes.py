from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from hades.assets.forms import RegistrationForm, LoginForm, ChangePasswordForm, AccountForm, PendingUserForm, ApprovedUserForm, CreateEventForm, ParticipantForm, PresentForm, AbsentForm
from hades.models.user import User
from hades.models.event import Event
from hades.models.access import Access
from hades.models.participant import Participant

import datetime

from hades import app, db, bcrypt, MASTER_PASSWORD

@app.route('/')
def index():
    events = Event.query.filter(Event.start_date >= datetime.date.today()).filter(Event.active_state==False)
    events = [event for event in events]
    if events:
        events.sort(key=lambda event : event.start_date)
    return render_template('index.html', title='Hades Lite', events=events)

@app.route('/<int:id>', methods=['POST', 'GET'])
def event(id):
    event = Event.query.filter_by(id=id).first()
    form = ParticipantForm(event_id=id)
    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.add(Participant(firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data, event_id=form.event_id.data))
            db.session.commit()
            flash('You have registered successfully', 'success')
            return redirect(url_for('event', id=form.event_id.data))
    if event:
        return render_template('event.html', title=event.name, event=event, form=form)
    else:
        return render_template('event.html', title='404', event=None)

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
            user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_passwd)
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
            elif user and not user.approved and bcrypt.check_password_hash(user.password, form.password.data):
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
        current_user.username = account_form.username.data.lower()
        current_user.email = account_form.email.data.lower()
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
    if request.method == 'POST':
        if request.form.get('approve'):
            return redirect(url_for('manage_user', action='approve', id=request.form.get('id')))
        elif request.form.get('reject'):
            return redirect(url_for('manage_user', action='reject', id=request.form.get('id')))
        elif request.form.get('delete'):
            return redirect(url_for('manage_user', action='delete', id=request.form.get('id')))
    users = User.query.all()
    approved_user_forms = {}
    pending_user_forms = {}
    for user in users:
        if user.approved:
            form = ApprovedUserForm(id=user.id)
            approved_user_forms[user.id] = [form, user.username, user.email]
        else:
            form = PendingUserForm(id=user.id)
            pending_user_forms[user.id] = [form, user.username, user.email]
    return render_template('users.html', title='Users', approved_user_forms=approved_user_forms, pending_user_forms=pending_user_forms)

@app.route('/admin/users/<string:action>/<int:id>')
@login_required
def manage_user(action, id):
    if int(id) == 1:
        flash('Cannot delete the master user', 'danger')
    elif current_user.id == 1:
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
    else:
        flash(f'You don\'t have sufficient rights.', 'danger')
    return redirect(url_for('users'))


@app.route('/admin/events/create-event', methods=['POST', 'GET'])
@login_required
def create_event():
    form = CreateEventForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            event = Event(
                name=form.name.data,
                description=form.description.data,
                start_date=form.start_date.data,
                start_time=form.start_time.data,
                end_date=form.end_date.data,
                end_time=form.end_time.data,
                event_creator=current_user.id,
                contact_email=form.contact_email.data
            )
            db.session.add(event)
            db.session.commit()
            event = Event.query.filter_by(name=form.name.data).first()
            access = Access(user_id=current_user.id, event_id=event.id)
            db.session.add(access)
            db.session.commit()
            flash('Event created successfully', 'success')
            return redirect(url_for('create_event'))
    return render_template('create_event.html', title='Create Event', form=form)

@app.route('/admin/events')
@login_required
def events():
    upcoming_events = []
    past_events = []
    events = Event.query.all()
    for event in events:
        if event.start_date < datetime.date.today():
            past_events.append(event)
        else:
            upcoming_events.append(event)
    if upcoming_events:
        upcoming_events.sort(key=lambda event : event.start_date)
    if past_events:
        past_events.sort(key=lambda event : event.start_date, reverse=True)
    return render_template('events.html', title='Events', upcoming_events=upcoming_events, past_events=past_events)

@app.route('/admin/events/<int:event_id>', methods=['POST', 'GET'])
@login_required
def view_participants(event_id):
    if request.method == 'POST':
        if request.form.get('mark_present'):
            return redirect(url_for('mark_attendance', event_id=event_id, action='mark_present', p_id=request.form.get('p_id')))
        elif request.form.get('mark_absent'):
            return redirect(url_for('mark_attendance', event_id=event_id, action='mark_absent', p_id=request.form.get('p_id')))
    event = Event.query.filter_by(id=event_id).first()
    if event and current_user in event.users:
        absent_forms = []
        present_forms = []
        for p in event.participants:
            print(p.id)
            if p.attended:
                form = PresentForm(p_id=p.id)
                present_forms.append([p, form])
            else:
                form = AbsentForm(p_id=p.id)
                absent_forms.append([p, form])
        return render_template('participants.html', title=event.name, event=event, present_forms=present_forms, absent_forms=absent_forms)
    elif event:
        flash('You Don\'t have access to this event.', 'danger')
        return redirect(url_for('events'))
    else:
        flash('Event you tried to access does not exists.', 'danger')
        return redirect(url_for('events'))

@app.route('/admin/events/<int:event_id>/<string:action>/<int:p_id>')
@login_required
def mark_attendance(event_id, action, p_id):
    participant = Participant.query.filter_by(id=p_id).first()
    if action=='mark_present':
        participant.attended = True
        db.session.add(participant)
        db.session.commit()
    elif action=='mark_absent':
        participant.attended = False
        db.session.add(participant)
        db.session.commit()
    else:
        flash('Action not recognized', 'danger')
    return redirect(url_for('view_participants', event_id=event_id))