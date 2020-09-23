#!/bin/bash
# Authors: David Dayan
# Used to run the flask site

# NOTE: it is recommended to use a pipenv virtual environment for managing packages and dependencies
# Also: run this script in the same directory as your application.py file
echo "enter application filename:"
read applicationName

export FLASK_APP=$applicationName
flask run
