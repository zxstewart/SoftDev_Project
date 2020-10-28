from flask_wtf import FlaskForm
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
    remember = BooleanField('Remeber Me')

class DownloadDataForm(FlaskForm):
    sport_type = SelectField(u'Sport Type', choices=[('team_sport', 'Team Sport'), ('individual_sport','Individual Sport')])
    sport = SelectField(u'Sport', choices=[('football','NFL Football'), ('baseball', 'MLB Baseball'), ('hockey', 'NHL Hockey'), ('basketball', 'NBA Basketball')])
    team = StringField('Team Name Abreviation: (First 3 Letters)', validators=[DataRequired(), Length(min=3,max=6)])
    season_year = StringField('Year of Season: XXXX', validators=[DataRequired(), Length(min=4,max=13)])
    submit = SubmitField('Fetch and Download Data')
