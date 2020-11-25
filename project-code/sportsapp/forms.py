from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
#make sure to also install email_validator: 'pipenv install email_validator'
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sportsapp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])   
    #email automatically checks that the provided email is valid! 
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    interests = StringField('Interests')
    submit = SubmitField('Sign Up')

    #adding custom validation to prevent users with duplicate usernames from being created
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken! Please choose a different one.')
    
    #adding custom validation to prevent users with duplicate emails from being created
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken or previously used! Please choose a different one.')

class LoginForm(FlaskForm):
    #login uses email over username
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

class DownloadDataForm(FlaskForm):
    sport_type = SelectField(u'Download Data Type', choices=[('season_schedule', 'Team Season Schedule'), ('league_stats','League-wide Stats by Team'), ('season_roster', 'Season Roster'), ('player_stats','Player Stats')])
    sport = SelectField(u'Sport', choices=[('football','NFL Football'), ('baseball', 'MLB Baseball'), ('hockey', 'NHL Hockey'), ('basketball', 'NBA Basketball')])
    team = SelectField(u'Team Name', choices=[])
    season_year = StringField('Year of Season: XXXX >1980', validators=[DataRequired(), Length(min=4,max=4)])
    players_list = SelectField('Select Players', choices=[])
    submit = SubmitField('Fetch and Download Data')

#account update form using registration form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])   
    #email automatically checks that the provided email is valid
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken! Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken or previously used! Please choose a different one.')

class FavoriteForm(FlaskForm):
    p_name = StringField('Player Name', validators=[DataRequired()])
    team = StringField('Team', validators=[DataRequired()])
    sport = StringField('Sport', validators=[DataRequired()])
    submit = SubmitField('Add to Favorites')


class ComparePlayersForm(FlaskForm):
    sport = SelectField(u'Sport', choices=[('nfl','Football'), ('mlb', 'Baseball'), ('nhl', 'Hockey'), ('nba', 'Basketball')])
    player1 = StringField('Name of player 1', validators=[DataRequired(), Length(min=3, max=50)])
    player2 = StringField('Name of player 2', validators=[DataRequired(), Length(min=3, max=50)])
    submit = SubmitField('Compare')