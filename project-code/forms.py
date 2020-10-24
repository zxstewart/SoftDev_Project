from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
#make sure to also install email_validator: 'pipenv install email_validator'
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])   
    #email automatically checks that the provided email is valid! 
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    interests = StringField('Interests')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    #login uses email over username
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remeber Me')

