#!/bin/bash
# Authors: David Dayan

#This script is used to run the local django server
#if debugging is set to true, the local server should auto refresh if changes are made and file saved

#ensure that python3 is installed and you have installed django through pip3

#run this program in the sports_stats_master directory
python3 manage.py runserver
