from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from decouple import config

DATABASE_NAME = config('DATABASE_NAME')
MASTER_USERNAME = config('MASTER_USERNAME')
MASTER_EMAIL = config('MASTER_EMAIL')
MASTER_PASSWORD = config('MASTER_PASSWORD')
SECRET_KEY = config('SECRET_KEY')

#create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_NAME+'.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "You need to be logged in to view this page"
login_manager.login_message_category = "danger"

from hades import routes
from hades.models.user import User
import os

if not os.path.isfile(os.path.join(os.getcwd(), 'hades', DATABASE_NAME+'.db')):
    db.create_all()
    master_user = User(username=MASTER_USERNAME, email=MASTER_EMAIL, password=bcrypt.generate_password_hash(MASTER_PASSWORD), approved=True)
    db.session.add(master_user)
    db.session.commit()