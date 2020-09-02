from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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
            DataRequired(),
        ]
    )
    remeber_me = BooleanField('Remeber Me')
    submit = SubmitField('Login')