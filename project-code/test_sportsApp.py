import pytest, tempfile, os, sportsapp
from sportsapp import app, db
from sportsapp.models import User, sportsStats, teamTable, Favorite


@pytest.fixture
def client():
    db_fd, sportsapp.app.config['DATABASE'] = tempfile.mkstemp()
    sportsapp.app.config['TESTING'] = True

    with sportsapp.app.test_client() as client:
        with sportsapp.app.app_context():
            sportsapp.__init__()
        yield client

    os.close(db_fd)
    os.unlink(sportsapp.app.config['DATABASE'])


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_login_logout(client):
    #Make sure login and logout works
    test = login(client, sportsapp.app.config['USERNAME'], sportsapp.app.config['PASSWORD'])
    assert b'You were logged in' in test.data

    test = logout(client)
    assert b'You were logged out' in test.data

    test = login(client, sportsapp.app.config['USERNAME'] + 'x', sportsapp.app.config['PASSWORD'])
    assert b'Invalid username' in test.data

    test = login(client, sportsapp.app.config['USERNAME'], sportsapp.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in test.data

def test_update_profile(client):
    #test user changing profile photo
    login(client, sportsapp.app.config['USERNAME'], sportsapp.app.config['PASSWORD'])
    test = client.post('/settings', data=dict(
        image_file='sportsapp/static/profileImages/fef05f17b42b8799.png',
    ), follow_redirects=True)
    assert b'No entries here so far' not in test.data
    assert b'<strong>HTML</strong> allowed here' in test.data