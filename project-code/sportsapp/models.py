from datetime import datetime
from sportsapp import db

class User(db.Model):
    #used for database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    #creating a one-to many relationship between users and their personal sports stats
    #owner attribute can be used to get the user who created the sportsStats
    posts = db.relationship('sportsStats', backref='owner', lazy=True)

    def __repr__(self):
        #magic method used for printing information in table
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#creating table for holding sports statistics
class sportsStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_queried = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"sportsStats('{self.title}', '{self.date_queried}')"
