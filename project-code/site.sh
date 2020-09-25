#!/bin/bash
# Authors: David Dayan
# Used to run the flask site

# NOTE: it is recommended to use a pipenv virtual environment for managing packages and dependencies
# Also: run this script in the same directory as your application.py file
echo "enter application filename:"
read applicationName

#runs the flask application in debug mode so we can see live reload
export FLASK_DEBUG=1

export FLASK_APP=$applicationName
flask run