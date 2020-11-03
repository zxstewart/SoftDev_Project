from flask import render_template, url_for, flash, redirect, request, send_from_directory, abort, send_file
import secrets
import os
from sportsapp import app, db, bcrypt
from sportsapp.forms import RegistrationForm, LoginForm, DownloadDataForm, UpdateAccountForm
#importing models for database
from sportsapp.models import User, sportsStats
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
from pathlib import Path

#using a list of dictionaries on local to just POC of passing dynamic content that will be eventually tied to database
information = [
    {
        'name': 'Peyton Manning',
        'position': 'Quarterback',
        'age': '44',
        'status': 'Old GOAT'
    },
    {
        'name': 'Jamal Murray',
        'position': 'Point Guard',
        'age': '23',
        'status': 'Maple Jordan'
    }
]

@app.route('/')
@app.route('/home')
def home():
    #can pass information (this would be from database calls eventually)
    return render_template('index.html', posts=information)

#browse page
@app.route('/browse')
def browse():
    return render_template('browse.html')

#adding routing backend for registration page
#NOTE: register.html is depracated and SHOULD NOT be used!
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        #This part of the code should be redundant because logout button replaces login and register buttons when user is logged in
        flash('You are already logged in!')
        return redirect(url_for('home'))
    form = RegistrationForm()
    #this will check if the form validated on POST
    if form.validate_on_submit():
        #generate a hashed password that will be put in database and will by encrypted with bcrypt: also decode to store the hash as string in db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, interest=form.interests.data)
        db.session.add(user)
        db.session.commit()
        #using f string because variable is passed in: 'success' is boostrap class 
        flash('Your account has been created and you are now able to log in!', 'success')
        return redirect(url_for('login'))
    # #can also pass and recieve form info (this will be implemented later)
    return render_template('registerNew.html', title='Register', form=form)

#adding routing backend for login page
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        #This part of the code should be redundant because logout button replaces login and register buttons when user is logged in
        flash('You are already logged in!')
        return redirect(url_for('home'))
    form = LoginForm()
    #this will check if the form validated on POST
    if form.validate_on_submit():
        #check database for validation of login POST
        user = User.query.filter_by(email=form.email.data).first()
        #check that user exists and that password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #login through the flask_login package that sets login state
            login_user(user, remember=form.remember.data)
            #find what page the user was trying to access before being redirected to login page
            next_page = request.args.get('next')
            #redirect the user to that page if they were trying to access a different page that required login
            flash('Successful Login Completed!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsucessful', 'danger')
    return render_template('login.html', title='Login',form=form)

#About page
@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

#Profile page
@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')

#video page
@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/football')
def football():
    return render_template('football.html')

@app.route('/basketball')
def basketball():
    return render_template('basketball.html')

@app.route('/hockey')
def hockey():
    return render_template('hockey.html')

@app.route('/soccer')
def soccer():
    return render_template('soccer.html')

@app.route('/baseball')
def baseball():
    return render_template('baseball.html')

#adding an app config to the generated files
app.config["SPORTS_DATA"] = "/static/sportsStatsDownloads"

@app.route('/download_data', methods=['GET','POST'])
def download_data():
    form = DownloadDataForm()
    #in each case I create a set of accepted team abbreviations for download_data (this is done dynamically b/c teams change over time)
    if form.validate_on_submit():
        if(form.sport.data == 'football'):
            #maybe later: create a drop down to select teams based on team name and abbreviations!
            from sportsreference.nfl.schedule import Schedule
            #also validating the team abbreviations for given year
            from sportsreference.nfl.teams import Teams
            teams = Teams(year=form.season_year.data)
            validAbbr = []
            for team in teams:
                validAbbr.append(team.abbreviation)
            validAbbrSet = set(validAbbr)
            #notify the user if an invalid abbreviation was inputted
            if form.team.data not in validAbbrSet:
                flash('Not a valid team abbreviation please try again', 'danger')
                return redirect(url_for('download_data'))
            teamData = Schedule(form.team.data, year=form.season_year.data)
            td = teamData.dataframe
            #maybe add a check for invalid 3 letter ID for team when inputting form
            p = Path("sportsapp").resolve()
            p = str(p) + "/static/sportsStatsDownloads/NFLSchedule_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
            td.to_csv(p, index=False)
            try:
                return send_file(p, as_attachment=True)
            except FileNotFoundError:
                abort(404)
        if(form.sport.data == 'baseball'):
            from sportsreference.mlb.schedule import Schedule
            #also validating the team abbreviations for given year
            from sportsreference.mlb.teams import Teams
            teams = Teams(year=form.season_year.data)
            validAbbr = []
            for team in teams:
                validAbbr.append(team.abbreviation)
            validAbbrSet = set(validAbbr)
            #notify the user if an invalid abbreviation was inputted
            if form.team.data not in validAbbrSet:
                flash('Not a valid team abbreviation please try again', 'danger')
                return redirect(url_for('download_data'))
            teamData = Schedule(form.team.data, year=form.season_year.data)
            td = teamData.dataframe
            p = Path("sportsapp").resolve()
            p = str(p) + "/static/sportsStatsDownloads/MLBSchedule_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
            td.to_csv(p, index=False)
            try:
                return send_file(p, as_attachment=True)
            except FileNotFoundError:
                abort(404)
        if(form.sport.data == 'hockey'):
            from sportsreference.nhl.schedule import Schedule
            #also validating the team abbreviations for given year
            from sportsreference.nhl.teams import Teams
            teams = Teams(year=form.season_year.data)
            validAbbr = []
            for team in teams:
                validAbbr.append(team.abbreviation)
            validAbbrSet = set(validAbbr)
            #notify the user if an invalid abbreviation was inputted
            if form.team.data not in validAbbrSet:
                flash('Not a valid team abbreviation please try again', 'danger')
                return redirect(url_for('download_data'))
            teamData = Schedule(form.team.data, year=form.season_year.data)
            td = teamData.dataframe
            p = Path("sportsapp").resolve()
            p = str(p) + "/static/sportsStatsDownloads/NHLSchedule_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
            td.to_csv(p, index=False)
            try:
                return send_file(p, as_attachment=True)
            except FileNotFoundError:
                abort(404)
        if(form.sport.data == 'baskeball'):
            from sportsreference.nba.schedule import Schedule
            #also validating the team abbreviations for given year
            from sportsreference.nba.teams import Teams
            teams = Teams(year=form.season_year.data)
            validAbbr = []
            for team in teams:
                validAbbr.append(team.abbreviation)
            validAbbrSet = set(validAbbr)
            #notify the user if an invalid abbreviation was inputted
            if form.team.data not in validAbbrSet:
                flash('Not a valid team abbreviation please try again', 'danger')
                return redirect(url_for('download_data'))
            teamData = Schedule(form.team.data, year=form.season_year.data)
            td = teamData.dataframe
            p = Path("sportsapp").resolve()
            p = str(p) + "/static/sportsStatsDownloads/NBASchedule_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
            td.to_csv(p, index=False)
            try:
                return send_file(p, as_attachment=True)
            except FileNotFoundError:
                abort(404)
    return render_template('download_data.html', title='Download Sports Data', form=form)

#adding routing backend for logout button
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#a route for editing account info (can only access while logged in)
#also uses @login_required decorator so /account page can only be accessed if logged in
#save picture function used when user changes profile image
def save_picture(form_picture):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = rand_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profileImages', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.interests = form.interests.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.interests.data = current_user.interests
    image_file = url_for('static', filename='profileImages/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form)