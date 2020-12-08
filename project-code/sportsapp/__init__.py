from flask import Flask
#importing the sqlalchemy for now, we can move to postgres for production LATER
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#initialize the imports
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#reroutes to login page if not logged in: called by login_required decorator
login_manager.login_view = 'login'
#make login messages use boostrap class
login_manager.login_message_category = 'info'

from sportsapp import routes