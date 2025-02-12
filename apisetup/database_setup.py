import sqlite3

# define connection and cursor

# create database
def create_database():
    connection = sqlite3.connect("local_player_info.db")
    cursor = connection.cursor()

    # create the players table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_info (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    team TEXT,
    position TEXT,
    headshot_url TEXT
    )

    '''

    )
    connection.commit()
    connection.close()
    print("Database created successfully")

if __name__ == "__main__":
    create_database()