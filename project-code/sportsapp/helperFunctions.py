#helper function for populating a list for a given year and sport
def teamChoices(sport, year):
    choices = []
    if sport == 'football':
        from sportsreference.nfl.teams import Teams
        teams = Teams(year=year)
        for team in teams:
            teamk = (team.abbreviation, team.name)
            choices.append(teamk)
        return choices
    if sport == 'hockey':
        from sportsreference.nhl.teams import Teams
        teams = Teams(year=year)
        for team in teams:
            teamk = (team.abbreviation, team.name)
            choices.append(teamk)
        return choices
    if sport == 'baseball':
        from sportsreference.mlb.teams import Teams
        teams = Teams(year=year)
        for team in teams:
            teamk = (team.abbreviation, team.name)
            choices.append(teamk)
        return choices
    if sport == 'basketball':
        from sportsreference.nfl.teams import Teams
        teams = Teams(year=year)
        for team in teams:
            teamk = (team.abbreviation, team.name)
            choices.append(teamk)
        return choices
    return choices
    