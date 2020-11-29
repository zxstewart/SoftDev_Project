# import pandas as pd
from prettytable import PrettyTable
  
csv_file = open('/Users/quinnstone/downloads/NFL_stats/Basic_Stats.csv', 'r')
csv_file = csv_file.readlines()
line_1 = csv_file[0]
line_1 = line_1.split(',')

x = PrettyTable([line_1[8],line_1[9],line_1[2],line_1[4],line_1[5],line_1[10],line_1[3]])

for a in range(1,17173):
    line = csv_file[a]
    line = line.split(',')
    if (line[3] == 'Active'):
        x.add_row([line[8],line[9],line[2],line[4],line[5],line[10],line[3]])
    else:
        pass

html_code = x.get_html_string()
html_file = open('/Users/quinnstone/Documents/203_4_F20/project-code/sportsapp/templates/Table.html', 'w')
html_file = html_file.write(html_code)
