from flask import Flask
#importing the sqlalchemy for now, we can move to postgres for production LATER
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#some generated list of 16 hex values (used for passwords and validation)
app.config['SECRET_KEY']='0819780287c1fe01cfb39284c1c55b7d'

#creating database on file system for now using sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#initialize the imports
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#reroutes to login page if not logged in: called by login_required decorator
login_manager.login_view = 'login'
#make login messages use boostrap class
login_manager.login_message_category = 'info'

from sportsapp import routes