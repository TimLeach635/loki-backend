from flask import jsonify, request

from app import app, db
from app.models.player import Player
from app.models.game import Game
from app.models.match import Match
from app.models.play import Play
from app.model_json import player_dict, game_dict, match_dict


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


@app.route('/players/')
@app.route('/players/<player_id>/')
def players_get(player_id=None):
    if player_id:
        player = Player.query.filter_by(player_id=player_id).first()
        return jsonify(player_dict(player)), 200
    else:
        player_list = Player.query.order_by(Player.player_id).all()
        player_list_dict = list(map(player_dict, player_list))
        return jsonify({'players': player_list_dict}), 200


@app.route('/players/', methods=['POST'])
def players_post():
    post_json = request.get_json()
    new_player = Player(first_name=post_json['first_name'], last_name=post_json['last_name'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify(player_dict(new_player)), 201


@app.route('/games/')
@app.route('/games/<game_id>/')
def games_get(game_id=None):
    if game_id:
        game = Game.query.filter_by(game_id=game_id).first()
        return jsonify(game_dict(game)), 200
    else:
        game_list = Game.query.order_by(Game.game_id).all()
        return jsonify({'games': list(map(game_dict, game_list))}), 200


@app.route('/games/', methods=['POST'])
def games_post():
    post_json = request.get_json()
    new_game = Game(name=post_json['name'])
    db.session.add(new_game)
    db.session.commit()
    return jsonify(game_dict(new_game)), 201


@app.route('/matches/')
@app.route('/matches/<match_id>/')
def matches_get(match_id=None):
    if match_id:
        match = Match.query.filter_by(match_id=match_id).first()
        return jsonify(match_dict(match)), 200
    else:
        match_list = Match.query.order_by(Match.match_id).all()
        return jsonify({'matches': list(map(match_dict, match_list))}), 200


@app.route('/matches/', methods=['POST'])
def matches_post():
    post_json = request.get_json()
    new_match = Match(game_id=post_json['game_id'], date=post_json['date'])
    db.session.add(new_match)
    db.session.commit()

    if 'winner_ids' in post_json.keys():
        for winner_id in post_json['winner_ids']:
            new_play = Play(match_id=new_match.match_id, player_id=winner_id, did_win=True)
            db.session.add(new_play)
        db.session.commit()

    if 'non_winner_ids' in post_json.keys():
        for non_winner_id in post_json['non_winner_ids']:
            new_play = Play(match_id=new_match.match_id, player_id=non_winner_id, did_win=False)
            db.session.add(new_play)
        db.session.commit()

    return jsonify(match_dict(new_match)), 201
