from flask import Flask
from flask_sqlalchemy import SQLAlchemy

database_name = 'test'
#create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'NeedToCreateEnvVariableForThis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+database_name+'.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from hades import routes