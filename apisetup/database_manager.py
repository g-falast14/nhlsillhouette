import sqlite3
import requests
import json

player_by_name = {}
TEAM_ABRS = ["BOS", "BUF", "DET", "FLA", "MTL", "OTT", "TBL", "TOR", "CAR", "CBJ", "NJD", "NYI", "NYR", "PHI", "PIT", "WSH", "UTA", "CHI", "COL", "DAL", "MIN", "NSH", "STL", "WPG", "ANA", "CGY", "EDM", "LAK", "SJS", "SEA", "VAN", "VGK"]


def save_players_to_db():
    """Saves all players from a dictionary into the database."""
    connection = sqlite3.connect('local_player_info.db')
    cursor = connection.cursor()

    for name in player_by_name:
        player_data = player_by_name[name] # grab player json
        player_id = player_data.get("id")  # Get player ID
        team = player_data.get("team")
        position = player_data.get("positionCode")
        headshot = player_data.get("headshot")

        # insert player info if it doesn't already exist
        cursor.execute('''
            INSERT OR IGNORE INTO local_player_info (player_id, name, team, position, headshot)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_id, name, team, position, headshot))

    connection.commit()
    connection.close()
    print(f"{len(player_by_name)} players saved successfully")

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


def update_players():

    # loop through every roster in the nhl
    for team in TEAM_ABRS:
        roster = get_json(f"https://api-web.nhle.com/v1/roster/{team}/current")
        print(team)
        for position, players in roster.items():  # Loop through forwards, defensemen, goalies
            for player in players:  # Loop through each player in the list
                full_name = f"{player['firstName']['default']} {player['lastName']['default']}"
                player_by_name[full_name] = player  # Store full player JSON


def print_json(data):
  print(json.dumps(data, indent=2))

def get_random_player(): # grab a random player from the database
    connection = sqlite3.connect(r"C:\Users\rgfal\OneDrive\Documents\NHLSillhouette\nhlsillhouette\apisetup\local_player_info.db")
    cursor = connection.cursor()

    # grab random player
    cursor.execute("SELECT * FROM local_player_info ORDER BY RANDOM() LIMIT 1;")
    player = cursor.fetchone()

    connection.close()

    if player:
        return player
    else:
        return None  # No players found




if __name__ == "__main__":
    print(get_random_player())
