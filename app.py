from flask import Flask, redirect, render_template, url_for, request, redirect, jsonify
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
    player = get_random_player()
    return render_template("game.html", player=player)

@app.route("/get-new-player")
def get_new_player():
    player = get_random_player()
    return jsonify(player)

if __name__ == "__main__":
    app.run(debug=True)