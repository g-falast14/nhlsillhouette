import sqlite3

def check_database():
    conn = sqlite3.connect("local_player_info.db")
    cursor = conn.cursor()

    # Retrieve all players from the database
    cursor.execute("SELECT * FROM player_info")
    players = cursor.fetchall()  # Fetch all rows

    conn.close()

    if not players:
        print("❌ Database is empty!")
    else:
        print("✅ Database is populated! Here are the players:")
        for player in players:
            print(player)

# Run the function when executing this file
if __name__ == "__main__":
    check_database()