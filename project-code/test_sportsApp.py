import pytest
from sportsapp import app


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_login_logout(client):
    #Make sure login and logout works

    user = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'])
    assert b'You were logged in' in user.data

    user = logout(client)
    assert b'You were logged out' in user.data

    user = login(client, flaskr.app.config['USERNAME'] + 'x', flaskr.app.config['PASSWORD'])
    assert b'Invalid username' in user.data

    user = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in user.data

def test_update_profile(client):
    #test user changing profile photo
    login(client, sportsapp.app.config['USERNAME'], sportsapp.app.config['PASSWORD'])
    user = client.post('/settings', data=dict(
        image_file='sportsapp/static/profileImages/fef05f17b42b8799.png',
    ), follow_redirects=True)
    assert b'No entries here so far' not in user.data
    assert b'<strong>HTML</strong> allowed here' in user.data