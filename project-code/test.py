from sportsreference.nfl.boxscore import Boxscore

game_data = Boxscore('201912220den')
print("The Denver Broncos scored: {} points".format(game_data.home_points))
print("The Detroit Lions scored: {} points".format(game_data.away_points))

df = game_data.dataframe
print(df.head(20))