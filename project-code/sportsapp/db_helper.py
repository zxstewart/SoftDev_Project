# Read the csv file using pandas to get the data
# open a sql connection to the database site.db
# insert the data that was read from the csv file into sql
# close the connection
# run python db_helper.py once
# commit the file site.db


import pandas as pd
import sqlalchemy as db
import pyodbc
from sqlalchemy import create_engine
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy


data = pd.read_csv(r'/Users/quinnstone/downloads/NFL_stats/Basic_Stats.csv')
df = pd.DataFrame(data, columns=['Name', 'College', 'Current Team', 'Experience', 'Position', 'Current Status', 'Years Played'])

# print(df)

# OBDC Driver
# conn = pyodbc.connect('DRIVER={Devart ODBC Driver for PostgreSQL};'
#                       'DATABASE=nfl_data;'
#                       'UID=postgres;'
#                       'PWD=Oliver101!;'
#                       'Trusted_Connection=yes;'
#                       'SERVER=localhost;'  # 127.0.0.1
#                       'PORT=5432;')
# cursor = conn.cursor()

# cursor.execute('SELECT * FROM database_name.table')

# for row in cursor:
#     print(row)

# config = dict(
#     server = 'localhost',
#     port = 5432,
#     database = 'nfl_data',
#     username = 'postgres',
#     password = 'Oliver101!')

# conn_str = (
#     'SERVER={server};' +
#     'PORT={port};' +
#     'DATABASE={database};' +
#     'UID={username};' +
#     'PWD={password}')

# conn = pyodbc.connect(
#     r'DRIVER={PostgreSQL Unicode(x64)};' +
#     conn_str.format(**config))

# engine = create_engine('sqlite:////Users/quinnstone/Documents/203_4_F20/project-code/sportsapp/site.db')

# sql_query = pd.read_sql_query('SELECT * FROM nfl_data', conn)
# print(sql_query)
# print(type(sql_query))

# cursor = cnxn.cursor()	
#     cursor.execute("SELECT * FROM nfl_data") 
#     row = cursor.fetchone() 
#     while row:
#     	print (row) 
#     	row = cursor.fetchone()

# for row in cursor:
#     print(row)

# cnxn = engine.raw_connection()
# server_name = cnxn.getinfo(pyodbc.SQL_SERVER_NAME)
# print(server_name)

# cursor.execute('CREATE TABLE nfl_data (Name nvarchar(50), College nvarchar(50), Current Team nvarchar(50), Experience nvarchar(50), Position nvarchar(50), nvarchar(20), nvarchar(50))')

# for row in df.itertuples():
#     cursor.execute('''
#                 INSERT INTO TestDB.dbo.people_info (Name, Country, Age)
#                 VALUES (?,?,?)
#                 ''',
#                 row.Name, 
#                 row.Country,
#                 row.Age
#                 )
# conn.commit()
# connection.close()
# brew install unixodbc, venv
