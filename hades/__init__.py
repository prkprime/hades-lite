from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

DATABASE_NAME = 'test'
MASTER_USERNAME = 'master'
MASTER_EMAIL = 'master@master.master'
MASTER_PASSWORD = 'password'
#create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'NeedToCreateEnvVariableForThis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_NAME+'.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "You need to be logged in to view this page"
login_manager.login_message_category = "danger"

from hades import routes