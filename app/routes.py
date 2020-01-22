from flask import jsonify, request
from app import app, db

@app.route('/')
@app.route('/index/')
def index():
    # Query database
    scoreboard = db.session.execute('SELECT first_name, last_name FROM players LIMIT 5;')

    # Convert result object to list of strings
    scoreboard_tuple_list = scoreboard.fetchall()
    scoreboard_string_list = map(lambda row: ' '.join(row), scoreboard_tuple_list)

    # Return JSON
    return jsonify({'scoreboard': list(scoreboard_string_list)})

@app.route('/players/', methods=['GET', 'POST'])
@app.route('/players/<player_id>/')
def players(player_id=None):
    if request.method == 'GET':
        if player_id:
            player = db.session.execute('SELECT player_id, first_name, last_name FROM players WHERE player_id = :player_id;', {'player_id': player_id}).first()
            return jsonify({'player_id': player[0], 'first_name': player[1], 'last_name': player[2]})
        else:
            players = db.session.execute('SELECT player_id, first_name, last_name FROM players;')
            return jsonify({'players': list(map(lambda player: {'player_id': player[0], 'first_name': player[1], 'last_name': player[2]}, players))})

@app.route('/games/')
@app.route('/games/<game_id>/')
def games(game_id=None):
    if request.method == 'GET':
        if game_id:
            game = db.session.execute('SELECT game_id, name FROM games WHERE game_id = :game_id;', {'game_id': game_id}).first()
            return jsonify({'game_id': game[0], 'name': game[1]})
        else:
            games = db.session.execute('SELECT game_id, name FROM games;')
            return jsonify({'games': list(map(lambda game: {'game_id': game[0], 'name': game[1]}, games))})

@app.route('/matches/')
@app.route('/matches/<match_id>/')
def matches(match_id=None):
    if request.method == 'GET':
        if match_id:
            match = db.session.execute(
                '''
                SELECT
                    matches.match_id AS match_id,
                    matches.date AS match_date,
                    games.name AS game_name
                FROM
                    matches LEFT JOIN games ON matches.game_id = games.game_id
                WHERE
                    match_id = :match_id;
                ''', {'match_id': match_id}).first()
            return jsonify({'match_id': match[0], 'match_date': match[1], 'game_name': match[2]})
        else:
            matches = db.session.execute(
                '''
                SELECT
                    matches.match_id AS match_id,
                    matches.date AS match_date,
                    games.name AS game_name
                FROM
                    matches LEFT JOIN games ON matches.game_id = games.game_id;
                ''', {'match_id': match_id})
            return jsonify({'matches': list(map(lambda match: {'match_id': match[0], 'match_date': match[1], 'game_name': match[2]}, matches))})
