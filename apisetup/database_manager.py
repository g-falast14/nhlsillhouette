import sqlite3
import requests
from apisetup.setup import player_by_name

player_by_name = {}
TEAM_ABRS = ["BOS", "BUF", "DET", "FLA", "MTL", "OTT", "TBL", "TOR", "CAR", "CBJ", "NJD", "NYI", "NYR", "PHI", "PIT", "WSH", "UTA", "CHI", "COL", "DAL", "MIN", "NSH", "STL", "WPG", "ANA", "CGY", "EDM", "LAK", "SJS", "SEA", "VAN", "VGK"]


def save_players_to_db(player_by_name):
    """Saves all players from a dictionary into the database."""
    connection = sqlite3.connect('local_player_info.db')
    cursor = connection.cursor()

    for name, data in player_by_name.items():
        player_id = data.get("id") # use .get() to avoid errors
        team = data.get("team")
        position = data.get("position")
        headshot_url = data.get("headshot_url")

        # insert player info if it doesn't already exist
        cursor.execute('''
            INSERT OR IGNORE INTO local_player_info (player_id, team, position, headshot_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_id, name, team, position, headshot_url))

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



if __name__ == "__main__":
    update_players()
    save_players_to_db(player_by_name)
