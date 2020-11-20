from flask import render_template, url_for, flash, redirect, request, send_from_directory, abort, send_file,jsonify
import secrets
import os
import sys
from sportsapp import app, db, bcrypt
from sportsapp.forms import RegistrationForm, LoginForm, DownloadDataForm, UpdateAccountForm, ComparePlayersForm
#importing models for database
from sportsapp.models import User, sportsStats, teamTable
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
from pathlib import Path
from sportsreference.nba.roster import Player

#generic list of dictionaries to be used when user is not loggedin
information = [
    {
        'title': 'See your generated files here!',
        'date': '',
        'fileName': 'Log in to see previously generated charts/downloaded data!'
    }
]

@app.route('/')
@app.route('/home')
def home():
    #check if user is loggedin
    if current_user.is_authenticated:
        #implementing database calls to fill dictionary passed to home page
        #home page will display previously generated data csv and charts
        #list of dictionaries for generated csv data
        csvList = []
        query = sportsStats.query.filter_by(user_id=current_user.id)
        for data in query:
            thisdict = dict(title=data.title, date=data.date_queried, fileName=data.downloaded_file)
            csvList.append(thisdict)
        return render_template('index.html', posts=csvList)
    else:
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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, interests=form.interests.data)
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

#Compare page
@app.route('/compare', methods=['GET','POST'])
def compare():
    form = ComparePlayersForm()
    if form.validate_on_submit():
        sport = form.sport.data
        player1 = form.player1.data
        player2 = form.player2.data
        #use to lookup player on API
        fname1id = player1.split()[0][0:2]
        lname1id = player1.split()[1][0:5]
        fname2id = player2.split()[0][0:2]
        lname2id = player2.split()[1][0:5]

        player1id = lname1id + fname1id+"01"
        player2id = lname2id + fname2id+"01"
        player1array = [1,2,3,4,5]
           # player2array = []

        data = {}
        data['value']=player1array
        return jsonify(data)

        playerobj1 = Player(player1id)
        playerobj2 = Player(player2id)
        
        if(form.sport.data == 'nba'):
            
            statnames = ['and-ones', 'assist_percentage', 'assists', 'block_percentage', 'blocking_fouls', 'blocks', 'box_plus_minus', 'center_percentage', 'defensive_box_plus_minus', 'defensive_rebound_percentage', 'turnovers', 'two_point_attempts', 'two_point_percentage', 'two_pointers', 'two_pointers_assisted_percentage', 'usage_percentage', 'value_over_replacement_player', 'weight', 'win_shares', 'win_shares_per_48_minutes']

            #can change to specify year
            playerobj1('2018-19')
            playerobj2('2018-19')

            player1array = [1,2,3,4,5]
            player2array = []

            data = {}
            data['value']=player1array
            return jsonify(data)
            #Need to get help
            # for i in statnames:
            #     player1array.append(playerobj1.i)
            #     player2array.append(playerobj2.i)
        
        elif(form.sport.data == 'mlb'):
            from sportsreference.mlb.roster import Player


       
    else:
        flash('Invalid input')
    return render_template('compare.html', title='Compare Stats', form=form)

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
@login_required
def download_data():
    form = DownloadDataForm()
    form.team.choices = [(team.team_abbr, team.team_name) for team in teamTable.query.all()]
    if form.validate_on_submit():
        if(form.sport.data == 'football'):
            from sportsreference.nfl.schedule import Schedule
            from sportsreference.nfl.teams import Teams
            teamData = Schedule(form.team.data, year=form.season_year.data)
            td = teamData.dataframe
            p = Path("sportsapp").resolve()
            f_n = "NFLSchedule_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
            p = str(p) + "/static/sportsStatsDownloads/" + f_n
            td.to_csv(p, index=False)
            #adding code to associate the downloaded file with the user
            nameDownload = "NFL Schedule: " + str(form.team.data) + " " + str(form.season_year.data)
            post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
            db.session.add(post)
            db.session.commit()
            try:
                return send_file(p, as_attachment=True)
            except FileNotFoundError:
                abort(404)
        if(form.sport.data == 'baseball'):
            from sportsreference.mlb.schedule import Schedule
            from sportsreference.mlb.teams import Teams
            teamData = Schedule(form.team.data, year=form.season_year.data)
            td = teamData.dataframe
            p = Path("sportsapp").resolve()
            f_n = "MLBSchedule_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
            p = str(p) + "/static/sportsStatsDownloads/" + f_n
            td.to_csv(p, index=False)
            #adding code to associate the downloaded file with the user
            nameDownload = "MLB Schedule: " + str(form.team.data) + " " + str(form.season_year.data)
            post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
            db.session.add(post)
            db.session.commit()
            try:
                return send_file(p, as_attachment=True)
            except FileNotFoundError:
                abort(404)
        if(form.sport.data == 'hockey'):
            from sportsreference.nhl.schedule import Schedule
            from sportsreference.nhl.teams import Teams
            teamData = Schedule(form.team.data, year=form.season_year.data)
            td = teamData.dataframe
            p = Path("sportsapp").resolve()
            f_n = "NHLSchedule_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
            p = str(p) + "/static/sportsStatsDownloads/" + f_n
            td.to_csv(p, index=False)
            #adding code to associate the downloaded file with the user
            nameDownload = "NHL Schedule: " + str(form.team.data) + " " + str(form.season_year.data)
            post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
            db.session.add(post)
            db.session.commit()
            try:
                return send_file(p, as_attachment=True)
            except FileNotFoundError:
                abort(404)
        if(form.sport.data == 'baskeball'):
            from sportsreference.nba.schedule import Schedule
            from sportsreference.nba.teams import Teams
            teamData = Schedule(form.team.data, year=form.season_year.data)
            td = teamData.dataframe
            p = Path("sportsapp").resolve()
            f_n = "NBASchedule_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
            p = str(p) + "/static/sportsStatsDownloads/" + f_n
            td.to_csv(p, index=False)
            #adding code to associate the downloaded file with the user
            nameDownload = "NBA Schedule: " + str(form.team.data) + " " + str(form.season_year.data)
            post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
            db.session.add(post)
            db.session.commit()
            try:
                return send_file(p, as_attachment=True)
            except FileNotFoundError:
                abort(404)
    return render_template('download_data.html', title='Download Sports Data', form=form)

#helper route function to return the teams in a year and for some sport
@app.route('/getnfl/<year>')
def getnfl(year):
    #query the database for the list of teams in football in the given year
    teams = teamTable.query.filter(teamTable.team_year==year).all()
    teamArr = []
    for team in teams:
        if team.sport == 'Football':
            teamObj = {}
            teamObj['abbr'] = team.team_abbr
            teamObj['name'] = team.team_name
            teamArr.append(teamObj)
    return jsonify({'teams' : teamArr})

@app.route('/getnba/<year>')
def getnba(year):
    teams = teamTable.query.filter(teamTable.team_year==year).all()
    teamArr = []
    for team in teams:
        if team.sport == 'Basketball':
            teamObj = {}
            teamObj['abbr'] = team.team_abbr
            teamObj['name'] = team.team_name
            teamArr.append(teamObj)
    return jsonify({'teams' : teamArr})

@app.route('/getnhl/<year>')
def getnhl(year):
    teams = teamTable.query.filter(teamTable.team_year==year).all()
    teamArr = []
    for team in teams:
        if team.sport == 'Hockey':
            teamObj = {}
            teamObj['abbr'] = team.team_abbr
            teamObj['name'] = team.team_name
            teamArr.append(teamObj)
    return jsonify({'teams' : teamArr})

@app.route('/getmlb/<year>')
def getmlb(year):
    teams = teamTable.query.filter(teamTable.team_year==year).all()
    teamArr = []
    for team in teams:
        if team.sport == 'Baseball':
            teamObj = {}
            teamObj['abbr'] = team.team_abbr
            teamObj['name'] = team.team_name
            teamArr.append(teamObj)
    return jsonify({'teams' : teamArr})

#Return CSV file (previously downloaded file)
@app.route('/<filename>', methods=['GET','POST'])
def getFile(filename):
    print('in function', file=sys.stderr)
    try:
        p = Path("sportsapp").resolve()
        p = str(p) + "/static/sportsStatsDownloads/" + filename
        return send_file(p, as_attachment=True)
    except FileNotFoundError:
        abort(404)

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
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profileImages/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form)

@app.route('/settings', methods=['GET','POST'])
def settings():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profileImages/' + current_user.image_file)
    return render_template('settings.html', title='Settings', image_file = image_file, form = form)

#code that initalizes the database teams
@app.route('/set_teamsNFL')
def setTeamsNFL():
    #using a loop to populate teams from year==1980 to present
    from sportsreference.nfl.teams import Teams
    for tY in range(1980, 2021):
        teams = Teams(year=tY)
        for team in teams:
            teamObj = teamTable(sport="Football", team_name=team.name, team_year=tY, team_abbr=team.abbreviation)
            db.session.add(teamObj)
            db.session.commit()
    flash('Loaded Teams for NFL into Database', 'success')
    return redirect(url_for('home'))

@app.route('/set_teamsNBA')
def setTeamsNBA():
    from sportsreference.nba.teams import Teams
    for tY in range(1980, 2021):
        teams = Teams(year=tY)
        for team in teams:
            teamObj = teamTable(sport="Basketball", team_name=team.name, team_year=tY, team_abbr=team.abbreviation)
            db.session.add(teamObj)
            db.session.commit()
    flash('Loaded Teams for NBA into Database', 'success')
    return redirect(url_for('home'))

@app.route('/set_teamsNHL')
def setTeamsNHL():
    from sportsreference.nhl.teams import Teams
    for tY in range(2010, 2020):
        teams = Teams(year=tY)
        for team in teams:
            teamObj = teamTable(sport="Hockey", team_name=team.name, team_year=tY, team_abbr=team.abbreviation)
            db.session.add(teamObj)
            db.session.commit()
    flash('Loaded Teams for NHL into Database', 'success')
    return redirect(url_for('home'))

@app.route('/set_teamsMLB')
def setTeamsMLB():
    from sportsreference.mlb.teams import Teams
    for tY in range(1980, 2021):
        teams = Teams(year=tY)
        for team in teams:
            teamObj = teamTable(sport="Baseball", team_name=team.name, team_year=tY, team_abbr=team.abbreviation)
            db.session.add(teamObj)
            db.session.commit()
    flash('Loaded Teams for MLB into Database', 'success')
    return redirect(url_for('home'))