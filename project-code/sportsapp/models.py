from datetime import datetime
from sportsapp import db, login_manager
from flask_login import UserMixin

#a function used by login_manager to define what user is currently acting as "client"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    #used for database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_profile.png')
    password = db.Column(db.String(60), nullable=False)
    #currently only support a single interest
    interests = db.Column(db.String(50), nullable=False)

    #creating a one-to-many relationship between users and their personal sports stats
    #owner attribute can be used to get the user who created the sportsStats
    posts = db.relationship('sportsStats', backref='owner', lazy=True)
    favPlay = db.relationship('Favorite', backref='owner', lazy=True)

    def __repr__(self):
        #magic method used for printing information in table
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Favorite(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(30))
    p_id = db.Column(db.String(30))
    team = db.Column(db.String(30))
    team_name = db.Column(db.String(30))
    sport = db.Column(db.String(30))
    sport_name = db.Column(db.String(30))
    weight = db.Column(db.String(4))
    height = db.Column(db.String(5))
    birthday = db.Column(db.String(15))
    games_played = db.Column(db.String(4))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Favorite('{self.p_name}', '{self.team}', '{self.sport}')"


#creating table for holding sports statistics
class sportsStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    downloaded_file = db.Column(db.String(30), nullable=False, default = '')
    date_queried = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"sportsStats('{self.title}', '{self.date_queried}')"

#creating table for holding team names, years, sport type
class teamTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String(10))
    team_name = db.Column(db.String(50))
    team_year = db.Column(db.Integer)
    team_abbr = db.Column(db.String(3))

#create all the tables before returning to importing file: ALL TABLES SHOULD BE DEFINED ABOVE THIS
db.create_all()