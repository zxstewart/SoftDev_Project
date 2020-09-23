Project Team Members:

David Dayan
Zoe Stewart
Mitchell LaRocque
John Lee
Makayla Johnson
---

## Contributors 
- David Dayan <david.dayan@colorado.edu>
- Zoe Stewart <zost6915@colorado.edu>
- Mitchell LaRocque <mila9009@colorado.edu>
- John Lee <jule8198@colorado.edu>
- Makayla Johnson <majo9858@colorado.edu>
---
# Development Process and Setup
## Setting up API calls to fetch data from Sports Reference
To begin using the sports reference API:

## Setting up virtual python environment for development
We will be using virtual python environments (pipenv) to separate python dev environment from other environments
### Installing pipenv and setting up virtual environment
Navigate to your directory that you will be using as a development environment then run: `pip3 install --user pipenv` to install pipenv package used to create virtual python environments

### ``pip3 list``
See what version all of your python packages are at

### Installing other python packages needed for the project development
Within your directory: we can now easily manage what versions/what packages we are using: numpy, flask, sports_referenceAPI, etc.
We can specify what versions we are using for this project and document that. These packages can be installed with a simple pip command: `pipenv install flask` or whatever package you want to install.

### Running project in pipenv
In command line run `pipenv run python3 -m flask run`: this will run a flask project in pipenv

### Other resources on virtual environments:
[Youtube Video Tutorial for Python Virtual Environments](https://www.youtube.com/watch?v=N5vscPTWKOk&list=PLVV11kd1LwZKub1q9KMC5FfQs8WPD_Aol&index=5&t=171s)
[Documentation for installing virtualenvs](https://docs.python-guide.org/dev/virtualenvs/)

NOTE: We don't need to keep track of our dependency and package version ourselves. Pipenv automatically takes care of that for us and stores it on Pipfile and Pipfile.lock
