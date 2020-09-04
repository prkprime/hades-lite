from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, Label, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from hades.models.user import User

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Length(min=2, max=15)
        ]
    )
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
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
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    update = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken. Please choose different username')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Account for this email is already created.')

class PendingUserForm(FlaskForm):
    username = StringField(
        'Username',
    )
    email = StringField(
        'Email'
    )
    approve = SubmitField('Approve')
    reject = SubmitField('Reject')

class ApprovedUserForm(FlaskForm):
    username = StringField(
        'Username',
    )
    email = StringField(
        'Email'
    )
    delete = SubmitField('Delete')