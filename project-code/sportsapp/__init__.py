from flask import Flask
#importing the sqlalchemy for now, we can move to postgres for production LATER
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#some generated list of 16 hex values (used for passwords and validation)
app.config['SECRET_KEY']='0819780287c1fe01cfb39284c1c55b7d'

#creating database on file system for now using sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from sportsapp import routes