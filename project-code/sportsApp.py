from flask import Flask, render_template, url_for
app = Flask(__name__)

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
    #can also pass and recieve form info (this will be implemented later)
    return render_template('register.html')

#adding routing backend for login page
@app.route('/login')
def login():
    #can also pass and recieve form info (this will be implemented later)
    return render_template('login.html')

#About page
@app.route('/about')
def about():
    return render_template('about.html')

#another way to run the application without using terminal
#simply run in terminal with python: $python3 sportsApp.py
if __name__ == '__main__':
    app.run(debug=True)
