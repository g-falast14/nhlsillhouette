from flask import Flask, redirect, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from flask import session
from datetime import timedelta
from apisetup.setup import get_random_player, update_players, player_by_name
from apisetup.database_manager import save_players_to_db


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content="Testing")

@app.route("/game", methods=["GET", "POST"])
def game():
    update_players() # run function to store jsons
    save_players_to_db(player_by_name)
    return render_template("game.html")




if __name__ == "__main__":
    app.run(debug=True)