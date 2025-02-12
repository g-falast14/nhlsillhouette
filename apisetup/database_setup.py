import sqlite3

# define connection and cursor

# create database
def create_database():
    connection = sqlite3.connect("local_player_info.db")
    cursor = connection.cursor()

    # create the players table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS local_player_info (
    player_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    team TEXT,
    position TEXT,
    headshot TEXT
    )

    '''

    )
    connection.commit()
    connection.close()
    print("Database created successfully")

import sqlite3

def check_tables():
    conn = sqlite3.connect("local_player_info.db")  # Update path if needed
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    conn.close()

    print("Tables in database:", tables)





if __name__ == "__main__":
    create_database()
    check_tables()