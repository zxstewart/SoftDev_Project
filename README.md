---
Project Team Members:
---

David Dayan
Zoe Stewart
Mitchell LaRocque
Quinn Stone
John Lee
Makayla Johnson

---

## Contributors 
- David Dayan <david.dayan@colorado.edu>
- Zoe Stewart <zost6915@colorado.edu>
- Mitchell LaRocque <mila9009@colorado.edu>
- Quinn Stone <qust3531@colorado.edu>
- John Lee <jule8198@colorado.edu>
- Makayla Johnson <majo9858@colorado.edu>
---
# Development Process and Setup
## Setting up Sports Reference API calls
To begin using the sports reference API and fetch data from the sports reference site:

### Installing ```sportsreference``` API through pipenv
Navigate to your your project and start your `pipenv` shell with the command `pipenv shell`. Once you have done this you can install the packages easily. Install `sportsreference` by using pipenv: `pipenv install sportsreference`

## Setting up virtual python environment for development
We will be using virtual python environments (pipenv) to separate python dev environment from other environments
### Installing pipenv and setting up virtual environment
Navigate to your directory that you will be using as a development environment then run: `pip3 install --user pipenv` to install pipenv package used to create virtual python environments

### See what version all of your python packages are at
`pipenv lock -r`

### Activate your pipenv environment.
`pipenv shell` You will install your packages from here. To quit the virtual environment pipenv: `exit` You can also run code in here too! (you should run code in here)

### Installing other python packages needed for the project development
Within your pipenv shell: we can now easily manage what versions/what packages we are using: numpy, flask, sports_referenceAPI, etc.
We can specify what versions we are using for this project and document that. These packages can be installed with a simple pip command: `pipenv install flask` or whatever package you want to install. If we want to install packages that are only used for development like test packages: `pipenv install nose --dev`. If you want to install packages from a requirements file: `pipenv install -r ./requirements.txt`

### Uninstalling python packages that were used in the pipenv
Run the command `pipenv uninstall flask`. To uninstall an instance of pipenv virtual environment: `pipenv --rm`

### Running project in pipenv
In (in pipenv shell) command line run `pipenv run python3 -m flask run`: this will run a flask project in pipenv

### Deploying code and ensuring web server uses correct version:
Make the server use the pipfile.lock to install the correct versions of packages. `pipenv lock` and then `pipenv install --ignore-pipfile`

### Other resources on virtual environments:
* [Youtube Video Tutorial for Pipenv and checking security/version vulnerabilities](https://www.youtube.com/watch?v=6Qmnh5C4Pmo)
* [Documentation for installing pipenv](https://docs.python-guide.org/dev/virtualenvs/)
* [Pipenv commmand cheatsheet](https://gist.github.com/bradtraversy/c70a93d6536ed63786c434707b898d55)

NOTE: We don't need to keep track of our dependency and package version ourselves. Pipenv automatically takes care of that for us and stores it on Pipfile and Pipfile.lock
