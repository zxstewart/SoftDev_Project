import pandas as pd
import numpy as np
from sportsreference.nfl.boxscore import Boxscore
from sportsreference.nfl.teams import Teams

game_data = Boxscore('201912220den')
print("The Denver Broncos scored: {} points".format(game_data.home_points))
print("The Detroit Lions scored: {} points".format(game_data.away_points))

#printing to explore what the NFL Teams contains
for team in Teams('2019'):
    print (team.name, team.wins, team.losses)
    #print(team.dataframe)

#retrieving a dataframe with a player's statistics from a certain season
df = game_data.dataframe
print(df.head(20))