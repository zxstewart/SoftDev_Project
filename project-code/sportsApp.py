from flask import Flask, render_template, url_for, flash, redirect
#from wtforms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY']=''

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
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerNew')
def registerNew():
    form = RegistrationForm()
    return render_template('registerNew.html', title='Register', form=form)

@app.route('/registerNew')
def registerNew():
    form = RegistrationForm()
    return render_template('registerNew.html', title='Register', form=form)

#adding routing backend for login page
@app.route('/login')
def login():
    #form = LoginForm()
    #can also pass and recieve form info (this will be implemented later)
    return render_template('login.html')

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

#another way to run the application without using terminal
#simply run in terminal with python: $python3 sportsApp.py
if __name__ == '__main__':
    app.run(debug=True)
