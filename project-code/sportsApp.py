from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return 'Hello, World!'

#about page
@app.route('/about')
def about():
    return '<h1>About page</h1>'

#another way to run the application without using terminal
#simply run in terminal with python: $python3 sportsApp.py
if __name__ == '__main__':
    app.run(debug=True)