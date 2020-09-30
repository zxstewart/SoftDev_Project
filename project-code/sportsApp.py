from flask import Flask, render_template
app = Flask(__name__)

#using a list of dictionaries on local to just POC of passing dynamic content that will be eventually tied to database
information = [
    {
        'name': 'Peyton Manning',
        'position': 'Quarterback',
        'age': '44'
    },
    {
        'name': 'Jamal Murray',
        'position': 'Point Guard',
        'age': '23'
    }
]

@app.route('/')
@app.route('/home')
def home():
    #can pass information (this would be from database calls eventually)
    return render_template('index.html', posts=information)

#about page
@app.route('/about')
def about():
    return '<h1>About page</h1>'

#another way to run the application without using terminal
#simply run in terminal with python: $python3 sportsApp.py
if __name__ == '__main__':
    app.run(debug=True)