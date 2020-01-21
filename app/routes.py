from flask import render_template
from app import app, db

@app.route('/')
@app.route('/index')
def index():
    scoreboard = db.session.execute('SELECT first_name, last_name FROM players;')
    return render_template('index.html', scoreboard=scoreboard)

@app.route('/players')
def players():
    players = db.session.execute('SELECT first_name, last_name FROM players;')
    return render_template('players.html', players=players)

@app.route('/games')
def games():
    games = db.session.execute('SELECT name FROM games;')
    return render_template('games.html', games=games)

@app.route('/matches')
def matches():
    matches = db.session.execute('SELECT date FROM matches;')
    return render_template('matches.html', matches=matches)
