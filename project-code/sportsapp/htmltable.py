import pandas as pd
from prettytable import PrettyTable

# Creates HTML for NFL Players

nfl_csv_file = open('/Users/quinnstone/downloads/NFL_stats/Basic_Stats.csv', 'r')
nfl_csv_file = nfl_csv_file.readlines()
nfl_line_1 = nfl_csv_file[0]
nfl_line_1 = nfl_line_1.split(',')

nfl_x = PrettyTable([nfl_line_1[8],nfl_line_1[9],nfl_line_1[2],nfl_line_1[4],nfl_line_1[5],nfl_line_1[10],nfl_line_1[3]])

for nfl_a in range(1,17173):
    nfl_line = nfl_csv_file[nfl_a]
    nfl_line = nfl_line.split(',')
    if (nfl_line[3] == 'Active'):
        nfl_x.add_row([nfl_line[8],nfl_line[9],nfl_line[2],nfl_line[4],nfl_line[5],nfl_line[10],nfl_line[3]])
    else:
        pass

nfl_html_code = nfl_x.get_html_string()
nfl_html_file = open('/Users/quinnstone/Documents/203_4_F20/project-code/sportsapp/templates/nfl_table.html', 'w')
nfl_html_file = nfl_html_file.write(nfl_html_code)

# -----------------------------------------------------------------------------------------------------------------------------------

# Creates HTML for NBA Players
  
nba_csv_file = open('/Users/quinnstone/downloads/all_seasons.csv', 'r')
nba_csv_file = nba_csv_file.readlines()
nba_line_1 = nba_csv_file[0]
nba_line_1 = nba_line_1.split(',')

nba_x = PrettyTable([nba_line_1[0], nba_line_1[1],nba_line_1[2],nba_line_1[3],nba_line_1[4],nba_line_1[5],nba_line_1[6],nba_line_1[7],nba_line_1[8],nba_line_1[9],nba_line_1[10],nba_line_1[11],nba_line_1[12],nba_line_1[13]])

for nba_a in range(1,515):
    nba_line = nba_csv_file[nba_a]
    nba_line = nba_line.split(',')
    nba_x.add_row([nba_line[0], nba_line[1],nba_line[2],nba_line[3],nba_line[4],nba_line[5],nba_line[6],nba_line[7],nba_line[8],nba_line[9],nba_line[10],nba_line[11],nba_line[12],nba_line[13]])

nba_html_code = nba_x.get_html_string()
nba_html_file = open('/Users/quinnstone/Documents/203_4_F20/project-code/sportsapp/templates/nba_table.html', 'w')
nba_html_file = nba_html_file.write(nba_html_code)

# -----------------------------------------------------------------------------------------------------------------------------------

# Creates HTML for MLB Players

mlb_csv_file = open('/Users/quinnstone/downloads/master.csv', 'r', encoding = "ISO-8859-1")
mlb_csv_file = mlb_csv_file.readlines()
mlb_line_1 = mlb_csv_file[0]
mlb_line_1 = mlb_line_1.split(',')

mlb_x = PrettyTable([mlb_line_1[0],mlb_line_1[1],mlb_line_1[2], mlb_line_1[3],mlb_line_1[4]])

for mlb_a in range(1,3308):
    mlb_line = mlb_csv_file[mlb_a]
    mlb_line = mlb_line.split(',')
    mlb_x.add_row([mlb_line[0], mlb_line[1],mlb_line[2],mlb_line[3],mlb_line[4]])

mlb_html_code = mlb_x.get_html_string()
mlb_html_file = open('/Users/quinnstone/Documents/203_4_F20/project-code/sportsapp/templates/mlb_table.html', 'w')
mlb_html_file = mlb_html_file.write(mlb_html_code)

# -----------------------------------------------------------------------------------------------------------------------------------

# Creates HTML for NHL Players

nhl_csv_file = open('/Users/quinnstone/downloads/skater_stats.csv', 'r',encoding = "ISO-8859-1")
nhl_csv_file = nhl_csv_file.readlines()
nhl_line_1 = nhl_csv_file[0]
nhl_line_1 = nhl_line_1.split(',')

nhl_x = PrettyTable([nhl_line_1[0],nhl_line_1[1],nhl_line_1[2],nhl_line_1[3],nhl_line_1[4]])

for nhl_a in range(1,891):
    nhl_line = nhl_csv_file[nhl_a]
    nhl_line = nhl_line.split(',')
    nhl_x.add_row([nhl_line[0], nhl_line[1],nhl_line[2],nhl_line[3],nhl_line[4]])

nhl_html_code = nhl_x.get_html_string()
nhl_html_file = open('/Users/quinnstone/Documents/203_4_F20/project-code/sportsapp/templates/nhl_table.html', 'w')
nhl_html_file = nhl_html_file.write(nhl_html_code)

# -----------------------------------------------------------------------------------------------------------------------------------

# Creates HTML for MLS Players

mls_csv_file = open('/Users/quinnstone/downloads/skater_stats.csv', 'r',encoding = "ISO-8859-1")
mls_csv_file = mls_csv_file.readlines()
mls_line_1 = mls_csv_file[0]
mls_line_1 = mls_line_1.split(',')

mls_x = PrettyTable([mls_line_1[0],mls_line_1[1],mls_line_1[2],mls_line_1[3],mls_line_1[4]])

for mls_a in range(1,617):
    mls_line = mls_csv_file[mls_a]
    mls_line = mls_line.split(',')
    mls_x.add_row([mls_line[0], mls_line[1],mls_line[2],mls_line[3],mls_line[4]])

mls_html_code = mls_x.get_html_string()
mls_html_file = open('/Users/quinnstone/Documents/203_4_F20/project-code/sportsapp/templates/mls_table.html', 'w')
mls_html_file = mls_html_file.write(mls_html_code)
