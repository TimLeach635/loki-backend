from flask import jsonify, request
from app import app, db
from app.models.player import Player

@app.route('/')
@app.route('/index/')
def index():
    scoreboard = db.session.execute('''
    SELECT
        players.first_name || ' ' || players.last_name AS player_name,
        COUNT (plays.did_win) AS player_wins
    FROM
        players LEFT JOIN plays ON players.player_id = plays.player_id
    WHERE
        plays.did_win = TRUE
    GROUP BY
        player_name;
    ''')

    scoreboard_tuple_list = scoreboard.fetchall()
    scoreboard_string_list = map(lambda row: {'player_name': row[0], 'player_wins': row[1]}, scoreboard_tuple_list)

    return jsonify({'scoreboard': list(scoreboard_string_list)})

@app.route('/players/', methods=['GET', 'POST'])
@app.route('/players/<player_id>/')
def players(player_id=None):
    if request.method == 'GET':
        if player_id:
            player = Player.query.filter_by(player_id=player_id).first()
            return jsonify({
                'player_id': player.player_id,
                'first_name': player.first_name,
                'last_name': player.last_name
            }), 200
        else:
            players = Player.query.order_by(Player.player_id).all()
            return jsonify({'players': list(map(lambda player: {
                'player_id': player.player_id,
                'first_name': player.first_name,
                'last_name': player.last_name
                }, players))}), 200
    elif request.method == 'POST':
        post_json = request.get_json()
        new_player = Player(first_name=post_json['first_name'], last_name=post_json['last_name'])
        db.session.add(new_player)
        db.session.commit()
        return jsonify({
            'player_id': new_player.player_id,
            'first_name': new_player.first_name,
            'last_name': new_player.last_name
        }), 201

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
