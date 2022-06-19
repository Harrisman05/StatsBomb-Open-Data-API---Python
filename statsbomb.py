import pandas as pd
from pandas import json_normalize
import requests
import random
from tabulate import tabulate

competitions = requests.get("https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json")
competitions = competitions.json()

champions_league_id = 16
season_id = []

# Extract all seasons that are in the Champions League competition

for competition_object in competitions:
    if competition_object['competition_name'] == 'Champions League':
        season_id.append(competition_object['season_id'])

# print(season_id)

## Generate a random season id from the season id list

random_season_id = random.choice(season_id)
# print(random_season_id)
# random_season_id = 37 # Milan vs Liverpool 2005      id 2 = Juventus vs Real Madrid 2017

# Using champions_league_id and random_season_id, generate a match id

match_object = requests.get(f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{str(champions_league_id)}/{str(random_season_id)}.json')
match_object = match_object.json()



# Extract Match ID from the generated match object

match_id = match_object[0]['match_id']
match_date = match_object[0]['match_date']
home_team = match_object[0]['home_team']['home_team_name']
away_team = match_object[0]['away_team']['away_team_name']
home_score = match_object[0]['home_score']
away_score = match_object[0]['away_score']


# Using match_id to generate event information

# Formations and lineups

event_object = requests.get(f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{str(match_id)}.json')
event_object = event_object.json()

home_team_tactical_data = event_object[0]
away_team_tactical_data = event_object[1]

home_team_formation = home_team_tactical_data['tactics']['formation']
away_team_formation = away_team_tactical_data['tactics']['formation']

# print(home_team_formation)
# print(away_team_formation)

home_team_lineup_object = home_team_tactical_data['tactics']['lineup']
away_team_lineup_object = away_team_tactical_data['tactics']['lineup']

both_lineups_object = [home_team_lineup_object, away_team_lineup_object]

home_team_lineup = [[' '], [home_team + ' --- ' + str(home_team_formation)], [' ']] # nested list so that tabulate works
away_team_lineup = [[' '], [away_team + ' --- ' + str(away_team_formation)], [' ']]
 
for data in both_lineups_object:

    for player_info in data:

        player_name = player_info['player']['name']
        player_number = player_info['jersey_number']
        player_position = player_info['position']['name']

        player_position_initials = ""

        player_position_2 = player_position.split(" ")

        for word in player_position_2:

            if word == "Goalkeeper":
                player_position_initials += 'GK'
            else:
                player_position_initials += word[0]

        tabulated_lineup = [str(player_number) + ' ' + player_name, player_position_initials]

        if len(home_team_lineup) != 14: # if home team lineup list is 11 (all players accounted for), then start appending to away_team_lineup
            home_team_lineup.append(tabulated_lineup)
        else:
            away_team_lineup.append(tabulated_lineup)


both_lineups = home_team_lineup + away_team_lineup

    
# print(home_team_lineup)
# print(away_team_lineup)

# Goal Events

goal_events_str = ''


for event in event_object:

    # Period 5 is extra time penalties. Needs to be excluded from goal count

    if event['type']['name'] == 'Shot' and event['shot']['outcome']['name'] == "Goal" and event["period"] != 5:

        # print(event['id'])

        timestamp = str(event["minute"]) + ':' + str(event["second"])
        goalscorer = event["player"]["name"]

        goal_event = goalscorer + ' - ' + timestamp
        goal_events_str += goal_event+'\n'


print(f'''

Champions League Final - {home_team} vs {away_team} - {match_date}

Final Score: {home_score}-{away_score}

{tabulate(both_lineups)}

Goalscorers

{goal_events_str}

''')



