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

#about page
@app.route('/browse')
def about():
    return render_template('browse.html')

#another way to run the application without using terminal
#simply run in terminal with python: $python3 sportsApp.py
if __name__ == '__main__':
    app.run(debug=True)