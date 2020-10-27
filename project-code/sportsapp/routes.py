from flask import render_template, url_for, flash, redirect
from sportsapp import app
from sportsapp.forms import RegistrationForm, LoginForm
#importing models for database
from sportsapp.models import User, sportsStats

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
    form = RegistrationForm()
    #this will check if the form validated on POST
    if form.validate_on_submit():
        #using f string because variable is passed in: 'success' is boostrap class 
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    # #can also pass and recieve form info (this will be implemented later)
    return render_template('registerNew.html', title='Register', form=form)

#adding routing backend for login page
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    #can also pass and recieve form info (this will be implemented later)
    #this will check if the form validated on POST
    if form.validate_on_submit():
        #using dummy to test validation of login POST
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Successful Login Completed!', 'success')
            return redirect(url_for('home'))
        #temp to call anything else besides hardcoded key to be failed login
        else:
            flash('Login Unsucessful', 'danger')
    return render_template('login.html', title='Login',form=form)

#About page
@app.route('/about')
def about():
    return render_template('about.html')

#Profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

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