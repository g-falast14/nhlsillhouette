# Imports
import sqlite3
import requests
import json
from functools import reduce
from operator import add
from tabulate import tabulate
import random

# team abbreviations
TEAM_ABRS = ["BOS", "BUF", "DET", "FLA", "MTL", "OTT", "TBL", "TOR", "CAR", "CBJ", "NJD", "NYI", "NYR", "PHI", "PIT", "WSH", "UTA", "CHI", "COL", "DAL", "MIN", "NSH", "STL", "WPG", "ANA", "CGY", "EDM", "LAK", "SJS", "SEA", "VAN", "VGK"]

# Empty dictionary to store { "Full Name": player_json }
player_by_name = {}

# Function to acquire json file
def get_json(url):
  try:
    response = requests.get(url, params={"Content-Type": "application/json"})
    response.raise_for_status()
  except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
    return
  except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
    return
  except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
    return
  except requests.exceptions.RequestException as err:
    print ("Oops: Something Else",err)
    return
  data = response.json()
  return data

# Function to print json data nicely
def print_json(data):
  print(json.dumps(data, indent=2))

def update_players():

    # loop through every roster in the nhl
    for team in TEAM_ABRS:
        roster = get_json(f"https://api-web.nhle.com/v1/roster/{team}/current")

        for position, players in roster.items():  # Loop through forwards, defensemen, goalies
            for player in players:  # Loop through each player in the list
                full_name = f"{player['firstName']['default']} {player['lastName']['default']}"
                player_by_name[full_name] = player  # Store full player JSON

    return player_by_name # return list of player names matching ids

def get_random_player():
    random_team = random.choice(TEAM_ABRS) # grab random team
    roster = get_json(f"https://api-web.nhle.com/v1/roster/{random_team}/current")

    all_players = []
    for category in roster:
        all_players.extend(roster[category]) # flatten json into a single list

    random_player = random.choice(all_players) # grab random player

    return random_player

if __name__ == "__main__":
    print(type(get_random_player()))