from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, Label, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.widgets import TextArea
from wtforms.fields.html5 import DateField, TimeField, EmailField
from flask_login import current_user

import datetime

from hades.models.user import User
from hades.models.event import Event
from hades.models.participant import Participant

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Length(min=2, max=15)
        ]
    )
    email = EmailField(
        'Email',
        validators = [
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=8, max=20)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose different username')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account for this email is already created.')

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Length(min=2, max=15)
        ]
    )
    password = PasswordField(
        'Password',
        validators = [
            DataRequired()
        ]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    new_password = PasswordField(
        'New Password',
        validators = [
            DataRequired(),
            Length(min=8, max=20)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('new_password')
        ]
    )
    update = SubmitField('Update')

class AccountForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Length(min=2, max=15)
        ]
    )
    email = EmailField(
        'Email',
        validators = [
            DataRequired()
        ]
    )
    update = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data.lower()).first()
            if user:
                raise ValidationError('Username is already taken. Please choose different username')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data.lower()).first()
            if user:
                raise ValidationError('Account for this email is already created.')

class PendingUserForm(FlaskForm):
    id = HiddenField()
    approve = SubmitField('Approve')
    reject = SubmitField('Reject')

class ApprovedUserForm(FlaskForm):
    id = HiddenField()
    delete = SubmitField('Delete')

class CreateEventForm(FlaskForm):
    name = StringField(
        'Event Name',
        validators = [
            DataRequired(),
            Length(max=100)
        ]
    )
    description = TextAreaField(
        'Event Description',
        validators = [
            DataRequired(),
            Length(max=500)
        ],
        widget = TextArea()
    )
    start_date = DateField(
        'Start Date',
        validators = [
            DataRequired()
        ]
    )
    start_time = TimeField(
        'Start Time',
        validators = [
            DataRequired()
        ]
    )
    end_date = DateField(
        'End Date',
        validators = [
            DataRequired()
        ]
    )
    end_time = TimeField(
        'End Time',
        validators = [
            DataRequired()
        ]
    )
    contact_email = EmailField(
        'Contact Email',
        validators = [
            DataRequired()
        ]
    )
    submit = SubmitField('Create')
   
    def validate_name(self, name):
        event = Event.query.filter_by(name=name.data).first()
        if event:
            raise ValidationError('Event Name already taken. Maybe try adding month or year or something unique to event name in case of event series')

    def validate_start_date(self, start_date):
        if start_date.data < datetime.date.today():
            raise ValidationError('You cannot set events in past mate')
    
    def validate_start_time(self, start_time):
        if self.start_date.data == datetime.date.today() and start_time.data < datetime.datetime.now().time():
            raise ValidationError('You cannot set events in past mate')
    
    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError('Event cannot finish before it starts you Dark fan')
    
    def validate_end_time(self, end_time):
        if self.start_date.data == self.end_date.data and end_time.data < self.start_time.data:
            raise ValidationError('Event cannot finish before it starts you Dark fan')

class ParticipantForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators = [
            DataRequired(),
            Length(max=100)
        ]
    )
    last_name = StringField(
        'Last Name',
        validators = [
            DataRequired(),
            Length(max=100)
        ]
    )
    email = EmailField(
        'Email',
        validators = [
            DataRequired()
        ]
    )
    event_id = HiddenField()
    submit = SubmitField('Register')

    def validate_email(self, email):
        participant = Participant.query.filter(Participant.email==email.data.lower()).filter(Participant.event_id==self.event_id.data).first()
        if participant:
            raise ValidationError('Entered Email has already registered for this event.')