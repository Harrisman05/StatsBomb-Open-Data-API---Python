import pandas as pd
from pandas import json_normalize
import requests
import random

# "name" : "Goal"

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
print(random_season_id)
random_season_id = 37 #      id 2 = Juventus vs Real Madrid 2017

# Using champions_league_id and random_season_id, generate a match id

match_object = requests.get(f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{str(champions_league_id)}/{str(random_season_id)}.json')
match_object = match_object.json()
# print(match_object)

# Extract Match ID from the generated match object

match_id = match_object[0]['match_id']
match_date = match_object[0]['match_date']
home_team = match_object[0]['home_team']['home_team_name']
away_team = match_object[0]['away_team']['away_team_name']

print(match_id)
print(match_date)
print(home_team)
print(away_team)

# Using match_id to generate event information

# Formations and lineups

event_object = requests.get(f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{str(match_id)}.json')
event_object = event_object.json()

home_team_tactical_data = event_object[0]
away_team_tactical_data = event_object[1]

home_team_formation = home_team_tactical_data['tactics']['formation']
away_team_formation = away_team_tactical_data['tactics']['formation']

print(home_team_formation)
print(away_team_formation)

home_team_lineup = home_team_tactical_data['tactics']['lineup']
away_team_lineup = away_team_tactical_data['tactics']['lineup']

both_lineups = [home_team_lineup, away_team_lineup]

for data in both_lineups:

    for player_info in data:

        player_name = player_info['player']['name']
        player_number = player_info['jersey_number']
        player_position = player_info['position']['name']

        print(f'{player_number} {player_name} - {player_position}')

    print(' ')
    
# Goal Events

for event in event_object:

    # Period 5 is extra time penalties. Needs to be excluded from goal count

    if event['type']['name'] == 'Shot' and event['shot']['outcome']['name'] == "Goal" and event["period"] != 5:

        # print(event['id'])

        timestamp = str(event["minute"]) + ':' + str(event["second"])
        goalscorer = event["player"]["name"]
        
        print(f'{goalscorer} - {timestamp}')

