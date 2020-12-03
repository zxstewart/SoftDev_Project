from flask import render_template, url_for, flash, redirect, request, send_from_directory, abort, send_file, jsonify
import secrets
import os
import sys
from sportsapp import app, db, bcrypt
from sportsapp.forms import RegistrationForm, LoginForm, DownloadDataForm, UpdateAccountForm, ComparePlayersForm, FavoriteForm
#importing models for database
from sportsapp.models import User, sportsStats, teamTable, Favorite
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
from pathlib import Path


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
    from sportsreference.nba.roster import Player
    form = ComparePlayersForm()
    if form.validate_on_submit():
        sport = form.sport.data
        player1 = form.player1.data.lower()
        player2 = form.player2.data.lower()
        #use to lookup player on API
        #Player object id's are formatted like "LLLLLFF01"
        fname1id = player1.split()[0][0:2]
        lname1id = player1.split()[1][0:5]
        fname2id = player2.split()[0][0:2]
        lname2id = player2.split()[1][0:5]

        player1id = lname1id + fname1id+"01"
        player2id = lname2id + fname2id+"01"

        if(sport == 'nba'):
            from sportsreference.nba.roster import Player
            player1stats = Player(player1id)
            player2stats = Player(player2id)
            #For the table
            df1 = player1stats.dataframe.loc['Career']
            df2 = player2stats.dataframe.loc['Career']
            #Check for NoneType *Not currently working
            if player1stats is None :
                flash('Invalid Player Name', 'danger')
                return render_template('compare.html', title='Compare Stats', form=form)
            if player2stats is None:
                flash('Invalid Player Name', 'danger')
                return render_template('compare.html', title='Compare Stats', form=form)
            #For Graph
            player1stats('career')
            player2stats('career')
            statnames = ["2 Pointers", "From 0-3 feet", "From 3-10 feet", "From 10-16 feet", '3 Pointers']
            p1data = [player1stats.two_point_percentage, player1stats.field_goal_perc_zero_to_three_feet, player1stats.field_goal_perc_three_to_ten_feet, player1stats.field_goal_perc_ten_to_sixteen_feet, player1stats.three_point_percentage]
            p2data = [player2stats.two_point_percentage, player2stats.field_goal_perc_zero_to_three_feet, player2stats.field_goal_perc_three_to_ten_feet, player2stats.field_goal_perc_ten_to_sixteen_feet, player2stats.three_point_percentage]
            #Changes None elements to 0.0
            for i in range(0, len(p1data)):
                if p1data[i] is None:
                    p1data[i] = 0.0

            for i in range(0, len(p2data)):
                if p2data[i] is None:
                    p2data[i] = 0.0

            df1.rename(index={'Career': player1})
            df2.rename(index={'Career': player2})
            concat = pd.concat([df1, df2]).T
            html_file = concat.to_html(classes='table table-striped table-bordered table-hover')
            return render_template('compare.html', form=form, statnames = statnames, p1name = form.player1.data, p2name = form.player2.data, p1data = p1data, p2data = p2data, tables = html_file)
        
        elif(sport == 'mlb'):
            from sportsreference.mlb.roster import Player
            player1stats = Player(player1id)
            player2stats = Player(player2id)
            #For the table
            df1 = player1stats.dataframe.loc['Career']
            df2 = player2stats.dataframe.loc['Career']
            #Check for NoneType *Not currently working
            if player1stats is None :
                flash('Invalid Player Name', 'danger')
                return render_template('compare.html', title='Compare Stats', form=form)
            if player2stats is None:
                flash('Invalid Player Name', 'danger')
                return render_template('compare.html', title='Compare Stats', form=form)
            #For Graph
            player1stats('career')
            player2stats('career')
            statnames = ["Fielding %", "% On Base", "Win %"]
            p1data = [player1stats.fielding_percentage, player1stats.on_base_percentage, player1stats.win_percentage]
            p2data = [player2stats.fielding_percentage, player2stats.on_base_percentage, player2stats.win_percentage]
            #Changes None elements to 0.0
            for i in range(0, len(p1data)):
                if p1data[i] is None:
                    p1data[i] = 0.0

            for i in range(0, len(p2data)):
                if p2data[i] is None:
                    p2data[i] = 0.0


            concat = pd.concat([df1, df2]).T
            html_file = concat.to_html(classes='table table-striped table-bordered table-hover')
            return render_template('compare.html', form=form, statnames = statnames, p1name = form.player1.data, p2name = form.player2.data, p1data = p1data, p2data = p2data, tables = html_file)
        

        elif(sport == "nfl"):
            from sportsreference.nfl.roster import Player
            #NFL uses a different id format "LLLLFF00"
            player1 = form.player1.data
            player2 = form.player2.data
            fname1id = player1.split()[0][0:2]
            lname1id = player1.split()[1][0:4]
            fname2id = player2.split()[0][0:2]
            lname2id = player2.split()[1][0:4]
            player1id = lname1id + fname1id+"00"
            player2id = lname2id + fname2id+"00"

            player1stats = Player(player1id)
            player2stats = Player(player2id)
            #For the table
            df1 = player1stats.dataframe.loc['Career']
            df2 = player2stats.dataframe.loc['Career']
            #Check for NoneType *Not currently working
            if player1stats is None :
                flash('Invalid Player Name', 'danger')
                return render_template('compare.html', title='Compare Stats', form=form)
            if player2stats is None:
                flash('Invalid Player Name', 'danger')
                return render_template('compare.html', title='Compare Stats', form=form)
            #For Graph
            player1stats('career')
            player2stats('career')
            statnames = ["Catch %", "Interception %", "Passing %"]
            p1data = [player1stats.catch_percentage, player1stats.interception_percentage, player1stats.passing_completion]
            p2data = [player2stats.catch_percentage, player2stats.interception_percentage, player2stats.passing_completion]            #Changes None elements to 0.0
            for i in range(0, len(p1data)):
                if p1data[i] is None:
                    p1data[i] = 0.0

            for i in range(0, len(p2data)):
                if p2data[i] is None:
                    p2data[i] = 0.0


            concat = pd.concat([df1, df2]).T
            html_file = concat.to_html(classes='table table-striped table-bordered table-hover')
            return render_template('compare.html', form=form, statnames = statnames, p1name = form.player1.data, p2name = form.player2.data, p1data = p1data, p2data = p2data, tables = html_file)
        
        elif(sport == 'nhl'):
            from sportsreference.nhl.roster import Player
            player1stats = Player(player1id)
            player2stats = Player(player2id)
            #For the table
            df1 = player1stats.dataframe.loc['Career']
            df2 = player2stats.dataframe.loc['Career']
            #Check for NoneType *Not currently working
            if player1stats is None :
                flash('Invalid Player Name', 'danger')
                return render_template('compare.html', title='Compare Stats', form=form)
            if player2stats is None:
                flash('Invalid Player Name', 'danger')
                return render_template('compare.html', title='Compare Stats', form=form)
            #For Graph
            player1stats('career')
            player2stats('career')
            statnames = ["Faceoff %", "PDO", "Shootout %"]
            p1data = [player1stats.faceoff_percentage, player1stats.pdo, player1stats.shootout_percentage]
            p2data = [player2stats.faceoff_percentage, player2stats.pdo, player2stats.shootout_percentage]
            #Changes None elements to 0.0
            for i in range(0, len(p1data)):
                if p1data[i] is None:
                    p1data[i] = 0.0

            for i in range(0, len(p2data)):
                if p2data[i] is None:
                    p2data[i] = 0.0


            concat = pd.concat([df1, df2]).T
            html_file = concat.to_html(classes='table table-striped table-bordered table-hover')
            return render_template('compare.html', form=form, statnames = statnames, p1name = form.player1.data, p2name = form.player2.data, p1data = p1data, p2data = p2data, tables = html_file)

       
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

@app.route('/other')
def other():
    return render_template('other.html')

#adding an app config to the generated files
app.config["SPORTS_DATA"] = "/static/sportsStatsDownloads"

@app.route('/download_data', methods=['GET','POST'])
@login_required
def download_data():
    form = DownloadDataForm()
    form.team.choices = [(team.team_abbr, team.team_name) for team in teamTable.query.all()]
    if form.validate_on_submit():
        if(form.sport.data == 'football'):
            if(form.sport_type.data == 'season_schedule'):
                from sportsreference.nfl.schedule import Schedule
                #from sportsreference.nfl.teams import Teams
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
            elif(form.sport_type.data == 'league_stats'):
                from sportsreference.nfl.teams import Teams
                team = Teams(year=form.season_year.data)
                td = team.dataframes
                p = Path("sportsapp").resolve()
                f_n = "NFL_League_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL League Stats: " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            elif(form.sport_type.data == 'player_stats'):
                #download the player's data in a season for a team
                from sportsreference.nfl.roster import Player
                player = Player(form.players_list.data)
                playYear = player(form.season_year.data)
                td = playYear.dataframe
                p = Path("sportsapp").resolve()
                f_n = "NFLRoster_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL Roster: " + str(form.team.data) + " " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            else:
                #generic response: returns the csv of list of teams in league in given year
                from sportsreference.nfl.teams import Teams
                teamData = Teams(year=form.season_year.data)
                td = teamData.dataframe
                p = Path("sportsapp").resolve()
                f_n = "NFL_League_Stats_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL Leaugue-Wide Stats: " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            
        if(form.sport.data == 'baseball'):
            if(form.sport_type.data == 'season_schedule'):
                from sportsreference.mlb.schedule import Schedule
                #from sportsreference.mlb.teams import Teams
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
            elif(form.sport_type.data == 'league_stats'):
                from sportsreference.mlb.teams import Teams
                team = Teams(year=form.season_year.data)
                td = team.dataframes
                p = Path("sportsapp").resolve()
                f_n = "MLB_League_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "MLB League Stats: " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            elif(form.sport_type.data == 'season_roster'):
                #populates dropdown of players on that teams roster: user can then download the specific forms
                from sportsreference.nfl.roster import Roster
                teamData = Roster(form.team.data, year=form.season_year.data)
                td = teamData.dataframe
                p = Path("sportsapp").resolve()
                f_n = "NFLRoster_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL Roster: " + str(form.team.data) + " " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            else:
                #generic response: returns the csv of list of teams in league in given year
                from sportsreference.nfl.teams import Teams
                teamData = Teams(year=form.season_year.data)
                td = teamData.dataframe
                p = Path("sportsapp").resolve()
                f_n = "NFL_League_Stats_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL Leaugue-Wide Stats: " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
        if(form.sport.data == 'hockey'):
            if(form.sport_type.data == 'season_schedule'):
                from sportsreference.nhl.schedule import Schedule
                #from sportsreference.nhl.teams import Teams
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
            elif(form.sport_type.data == 'league_stats'):
                from sportsreference.nhl.teams import Teams
                team = Teams(year=form.season_year.data)
                td = team.dataframes
                p = Path("sportsapp").resolve()
                f_n = "NHL_League_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NHL League Stats: " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            elif(form.sport_type.data == 'season_roster'):
                #populates dropdown of players on that teams roster: user can then download the specific forms
                from sportsreference.nfl.roster import Roster
                teamData = Roster(form.team.data, year=form.season_year.data)
                td = teamData.dataframe
                p = Path("sportsapp").resolve()
                f_n = "NFLRoster_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL Roster: " + str(form.team.data) + " " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            else:
                #generic response: returns the csv of list of teams in league in given year
                from sportsreference.nfl.teams import Teams
                teamData = Teams(year=form.season_year.data)
                td = teamData.dataframe
                p = Path("sportsapp").resolve()
                f_n = "NFL_League_Stats_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL Leaugue-Wide Stats: " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
        if(form.sport.data == 'baskeball'):
            if(form.sport_type.data == 'season_schedule'):
                from sportsreference.nba.schedule import Schedule
                #from sportsreference.nba.teams import Teams
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
            elif(form.sport_type.data == 'league_stats'):
                from sportsreference.nba.teams import Teams
                team = Teams(year=form.season_year.data)
                td = team.dataframes
                p = Path("sportsapp").resolve()
                f_n = "NBA_League_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NBA League Stats: " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            elif(form.sport_type.data == 'season_roster'):
                #populates dropdown of players on that teams roster: user can then download the specific forms
                from sportsreference.nfl.roster import Roster
                teamData = Roster(form.team.data, year=form.season_year.data)
                td = teamData.dataframe
                p = Path("sportsapp").resolve()
                f_n = "NFLRoster_" + str(form.team.data) + "_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL Roster: " + str(form.team.data) + " " + str(form.season_year.data)
                post = sportsStats(title=nameDownload, downloaded_file=f_n, owner=current_user)
                db.session.add(post)
                db.session.commit()
                try:
                    return send_file(p, as_attachment=True)
                except FileNotFoundError:
                    abort(404)
            else:
                #generic response: returns the csv of list of teams in league in given year
                from sportsreference.nfl.teams import Teams
                teamData = Teams(year=form.season_year.data)
                td = teamData.dataframe
                p = Path("sportsapp").resolve()
                f_n = "NFL_League_Stats_" + str(form.season_year.data) + ".csv"
                p = str(p) + "/static/sportsStatsDownloads/" + f_n
                td.to_csv(p, index=False)
                #adding code to associate the downloaded file with the user
                nameDownload = "NFL Leaugue-Wide Stats: " + str(form.season_year.data)
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
    image_file = url_for('static', filename='profileImages/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file)

@app.route('/faveList', methods=['GET','POST'])
@login_required
def favorite_list():
    favorite = Favorite.query.all()
    return render_template('faveList.html', title='My Favorite Players', favorite=favorite)

@app.route('/favorites', methods=['GET','POST'])
@login_required
def favorite():
    form = FavoriteForm()
    if form.validate_on_submit():
        #the data from the form is the abbreviation of the team and the abbreviation of the player name
        #convert and add relevant info about player to the database
        if(str(form.sport.data) == 'mlb'):
            from sportsreference.mlb.roster import Player
            player = Player(form.p_name.data)
            favorite = Favorite(p_name=player.name, p_id=form.p_name.data, team=form.team.data, team_name=form.team.name, sport=form.sport.data, sport_name='Football', weight=player.weight, height=player.height, birthday=player.birth_date, games_played=player.games)
            db.session.add(favorite) 
            db.session.commit()
        if(str(form.sport.data) == 'nba'):
            from sportsreference.nba.roster import Player
            player = Player(form.p_name.data)
            favorite = Favorite(p_name=player.name, p_id=form.p_name.data, team=form.team.data, team_name=form.team.name, sport=form.sport.data, sport_name='Basketball', weight=player.weight, height=player.height, birthday=player.birth_date, games_played=player.games)
            db.session.add(favorite) 
            db.session.commit()
        if(str(form.sport.data) == 'nhl'):
            from sportsreference.nhl.roster import Player
            player = Player(form.p_name.data)
            favorite = Favorite(p_name=player.name, p_id=form.p_name.data, team=form.team.data, team_name=form.team.name, sport=form.sport.data, sport_name='Hockey', weight=player.weight, height=player.height, birthday=player.birth_date, games_played=player.games)
            db.session.add(favorite) 
            db.session.commit()
        else:
            from sportsreference.nfl.roster import Player
            player = Player(form.p_name.data)
            favorite = Favorite(p_name=player.name, p_id=form.p_name.data, team=form.team.data, team_name=form.team.name, sport=form.sport.data, sport_name='Baseball', weight=player.weight, height=player.height, birthday=player.birth_date, games_played=player.games)
            db.session.add(favorite) 
            db.session.commit()
        flash('Player has been added', 'success')
        return redirect(url_for('account'))
    return render_template('favorites.html', title='Add Favorite', form=form, legend='Add Favorite')

@app.route('/favorites/<int:favorite_id>', methods=['GET','POST'])
def view_favorite(favorite_id):
    favorite = Favorite.query.filter_by(id=favorite_id).first()
    sport = favorite.sport

    player1id = favorite.p_id
    if(sport == 'nba'):
        from sportsreference.nba.roster import Player
        player1stats = Player(player1id)

        #For the table
        df1 = player1stats.dataframe.loc['Career']
        #Check for NoneType *Not currently working
        if player1stats is None :
            flash('Invalid Player Name', 'danger')
            return render_template('compare.html', title='Compare Stats')
        #For Graph
        player1stats('career')
        statnames = ["2 Pointers", "From 0-3 feet", "From 3-10 feet", "From 10-16 feet", '3 Pointers']
        p1data = [player1stats.two_point_percentage, player1stats.field_goal_perc_zero_to_three_feet, player1stats.field_goal_perc_three_to_ten_feet, player1stats.field_goal_perc_ten_to_sixteen_feet, player1stats.three_point_percentage]
        #Changes None elements to 0.0
        for i in range(0, len(p1data)):
            if p1data[i] is None:
                p1data[i] = 0.0


        df1.rename(index={'Career': player1})
        df1 = df1.T
        html_file = df1.to_html(classes='table table-striped table-bordered table-hover')
        return render_template('fPlayer.html', title=favorite.p_name, favorite=favorite, statnames = statnames, p1data = p1data, tables = html_file, name = pname)
    
    elif(sport == 'mlb'):
        from sportsreference.mlb.roster import Player
        player1stats = Player(player1id)
        #For the table
        df1 = player1stats.dataframe.loc['Career']
        #Check for NoneType *Not currently working
        if player1stats is None :
            flash('Invalid Player Name', 'danger')
            return render_template('compare.html', title='Compare Stats')
        #For Graph
        player1stats('career')
        statnames = ["Fielding %", "% On Base", "Win %"]
        p1data = [player1stats.fielding_percentage, player1stats.on_base_percentage, player1stats.win_percentage]
        #Changes None elements to 0.0
        for i in range(0, len(p1data)):
            if p1data[i] is None:
                p1data[i] = 0.0

        concat = df1.T
        html_file = concat.to_html(classes='table table-striped table-bordered table-hover')
        return render_template('fPlayer.html', title=favorite.p_name, favorite=favorite, statnames = statnames, p1data = p1data, tables = html_file, name = pname)    

    elif(sport == "nfl"):
        from sportsreference.nfl.roster import Player
        #NFL uses a different id format "LLLLFF00"
        player1id = favorite.p_id
        player1stats = Player(player1id)
        #For the table
        df1 = player1stats.dataframe.loc['Career']
        #Check for NoneType *Not currently working
        if player1stats is None :
            flash('Invalid Player Name', 'danger')
            return render_template('compare.html', title='Compare Stats')
        #For Graph
        player1stats('career')
        statnames = ["Catch %", "Interception %", "Passing %"]
        p1data = [player1stats.catch_percentage, player1stats.interception_percentage, player1stats.passing_completion]
        for i in range(0, len(p1data)):
            if p1data[i] is None:
                p1data[i] = 0.0

        concat = df1.T
        html_file = concat.to_html(classes='table table-striped table-bordered table-hover')
        imgSrc = 'https://pro-football-reference.com/req/20200210/images/headshots/' + favorite.p_id + '.jpg'
        return render_template('fPlayer.html', title=favorite.p_name, favorite=favorite, statnames = statnames, p1data = p1data, tables = html_file, image=imgSrc)

    elif(sport == 'nhl'):
        from sportsreference.nhl.roster import Player
        player1stats = Player(player1id)
        #For the table
        df1 = player1stats.dataframe.loc['Career']
        #Check for NoneType *Not currently working
        if player1stats is None :
            flash('Invalid Player Name', 'danger')
            return render_template('compare.html', title='Compare Stats', form=form)
        #For Graph
        player1stats('career')
        statnames = ["Faceoff %", "PDO", "Shootout %"]
        p1data = [player1stats.faceoff_percentage, player1stats.pdo, player1stats.shootout_percentage]
        #Changes None elements to 0.0
        for i in range(0, len(p1data)):
            if p1data[i] is None:
                p1data[i] = 0.0


        concat = df1.T
        html_file = concat.to_html(classes='table table-striped table-bordered table-hover')
        return render_template('fPlayer.html', title=favorite.p_name, favorite=favorite, statnames = statnames, p1data = p1data, tables = html_file, name = pname)
       
    else:
        flash('Invalid input')
        return render_template('fPlayer.html', title=favorite.p_name, favorite=favorite)

@app.route('/favorites/<int:favorite_id>/update', methods=['GET','POST'])
def update_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)
    form = FavoriteForm()
    if form.validate_on_submit():
        favorite.p_name = form.p_name.data
        favorite.team = form.team.data
        favorite.sport = form.sport.data
        db.session.commit()
        flash('Player has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.p_name.data = favorite.p_name
        form.team.data = favorite.team
        form.sport.data = favorite.sport
    return render_template('favorites.html', title='Update Favorite', form=form, legend='Update Favorite')

@app.route('/favorites/<int:favorite_id>/delete', methods=['POST'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    flash('Player has been deleted from Favorites', 'success')
    return redirect(url_for('account'))

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

#app route for generating nice view of data in table form
@app.route('/viewData/<filename>')
def viewData(filename):
    #stz = 'Able to go to viewData route ' + filename
    #flash(stz, 'success')
    try:
        p = Path("sportsapp").resolve()
        p = str(p) + "/static/sportsStatsDownloads/" + filename
        table = pd.read_csv(p)
        html_file = table.to_html(classes='table table-striped table-bordered table-hover')
        nameTable = filename[0:-4]
        nameTable = nameTable.replace("_"," ")
        return render_template('view_table.html', title='View Table', tables=html_file, table_name=nameTable)
    except FileNotFoundError:
        abort(404)

#app route for returning a json filled with player ids and names
@app.route('/getPlayers/')
def getPlayers():
    team = request.args.get('team')
    year = request.args.get('year')
    sport = request.args.get('sport')

    playerArr = []
    #now getting the players object from sportsreference API
    #choose correct api object based on sport type
    if(sport == 'football'):
        from sportsreference.nfl.roster import Roster
        roster = Roster(team, year=year, slim=True)
        players = roster.players
        for play_id, play_name in players.items():
            playerObj = {}
            playerObj['play_id'] = play_id
            playerObj['play_name'] = play_name
            playerArr.append(playerObj)
        return jsonify({'players' : playerArr})
    elif(sport == 'baseball'):
        from sportsreference.mlb.roster import Roster
        roster = Roster(team, year=year, slim=True)
        players = roster.players
        for play_id, play_name in players.items():
            playerObj = {}
            playerObj['play_id'] = play_id
            playerObj['play_name'] = play_name
            playerArr.append(playerObj)
        return jsonify({'players' : playerArr})
    elif(sport == 'hockey'):
        from sportsreference.nhl.roster import Roster
        roster = Roster(team, year=year, slim=True)
        players = roster.players
        for play_id, play_name in players.items():
            playerObj = {}
            playerObj['play_id'] = play_id
            playerObj['play_name'] = play_name
            playerArr.append(playerObj)
        return jsonify({'players' : playerArr})
    else:
        from sportsreference.nba.roster import Roster
        roster = Roster(team, year=year, slim=True)
        players = roster.players
        for play_id, play_name in players.items():
            playerObj = {}
            playerObj['play_id'] = play_id
            playerObj['play_name'] = play_name
            playerArr.append(playerObj)
        return jsonify({'players' : playerArr})

#app route for returning a json filled with player ids and names
@app.route('/getFavoritePlayers/')
def getFavoritePlayers():
    team = request.args.get('team')
    sport = request.args.get('sport')

    playerArr = []
    #now getting the players object from sportsreference API: choose correct api object based on sport type
    if(sport == 'nfl'):
        from sportsreference.nfl.roster import Roster
        for year in range(1980,2021):
            roster = Roster(team, year=year, slim=True)
            players = roster.players
            for play_id, play_name in players.items():
                playerObj = {}
                playerObj['play_id'] = play_id
                playerObj['play_name'] = play_name
                playerArr.append(playerObj)
    elif(sport == 'mlb'):
        from sportsreference.mlb.roster import Roster
        for year in range(1980, 2021):
            roster = Roster(team, year=year, slim=True)
            players = roster.players
            for play_id, play_name in players.items():
                playerObj = {}
                playerObj['play_id'] = play_id
                playerObj['play_name'] = play_name
                playerArr.append(playerObj)
    elif(sport == 'nhl'):
        from sportsreference.nhl.roster import Roster
        for year in range(2010,2020):
            roster = Roster(team, year=year, slim=True)
            players = roster.players
            for play_id, play_name in players.items():
                playerObj = {}
                playerObj['play_id'] = play_id
                playerObj['play_name'] = play_name
                playerArr.append(playerObj)
    else:
        from sportsreference.nba.roster import Roster
        for year in range(1980, 2021):
            roster = Roster(team, year=year, slim=True)
            players = roster.players
            for play_id, play_name in players.items():
                playerObj = {}
                playerObj['play_id'] = play_id
                playerObj['play_name'] = play_name
                playerArr.append(playerObj)
    #remove duplicates from the list of dictionaries
    setPlayers = [dict(t) for t in {tuple(d.items()) for d in playerArr}]
    return jsonify({'players' : setPlayers})

#an app route that returns a json from a python set of teams based on sport
@app.route('/getAllTeams/<sport>')
def getAllTeams(sport):
    teamChoices = []
    if sport == 'nfl':
        for team in teamTable.query.filter_by(sport='Football'):
            teamObj = {}
            teamObj['abbr'] = team.team_abbr
            teamObj['name'] = team.team_name
            teamChoices.append(teamObj)
    elif sport == 'nhl':
        for team in teamTable.query.filter_by(sport='Hockey'):
            teamObj = {}
            teamObj['abbr'] = team.team_abbr
            teamObj['name'] = team.team_name
            teamChoices.append(teamObj)
    elif sport == 'mlb':
        for team in teamTable.query.filter_by(sport='Baseball'):
            teamObj = {}
            teamObj['abbr'] = team.team_abbr
            teamObj['name'] = team.team_name
            teamChoices.append(teamObj)
    else:
        for team in teamTable.query.filter_by(sport='Basketball'):
            teamObj = {}
            teamObj['abbr'] = team.team_abbr
            teamObj['name'] = team.team_name
            teamChoices.append(teamObj)
    #convert a list of 
    teamChoicesSet = [dict(t) for t in {tuple(d.items()) for d in teamChoices}]
    return jsonify({'teams' : teamChoicesSet})