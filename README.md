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
We will be using virtual python environments (virtualenv) to separate python dev environment from other environments
### ``pip3 install virtualenv``
This installs virtualenv package used to create virtual python environments
### ``pip3 list``
See what version all of your python packages are at
### ``virtualenv project1_env``
Use this to create a new python virtual environment and you should create this on some local directory.
### ``source project1_env/bin/activate``
This will create a new virtual environment where we can now easily manage what versions/what packages we are using: numpy, flask, sports_referenceAPI, etc.
### Installing other python packages needed for the project development
We can specify what versions we are using for this project and document that. These packages can be installed with a simple pip command: `pip install numpy` or whatever package you want to install. You can also run a text file filled with versions that will be provided so we can maintain the same versions on this site: `pip install -r requirements.txt`
### Exporting VirtualEnvironment Package Version 
`pip3 freeze --local > requirements.txt` to store all dependencies/package version into a text file
### Exit Virtual environment
`deactivate`
### Other resources on virtual environments:
[Youtube Video Tutorial for Python Virtual Environments](https://www.youtube.com/watch?v=N5vscPTWKOk&list=PLVV11kd1LwZKub1q9KMC5FfQs8WPD_Aol&index=5&t=171s)
