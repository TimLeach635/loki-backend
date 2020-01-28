from flask import jsonify, request
from app import app, db
from app.models.player import Player
from app.models.game import Game
from app.models.match import Match
from app.models.play import Play

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
                'last_name': player.last_name,
                'plays': list(map(lambda play: {
                    'play_id': play.play_id,
                    'match_id': play.match_id,
                    'match_date': play.match.date,
                    'game_id': play.match.game.game_id,
                    'game_name': play.match.game.name,
                    'did_win': play.did_win
                }, player.plays))
            }), 200
        else:
            players = Player.query.order_by(Player.player_id).all()
            return jsonify({'players': list(map(lambda player: {
                'player_id': player.player_id,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'plays': list(map(lambda play: {
                    'play_id': play.play_id,
                    'match_id': play.match_id,
                    'match_date': play.match.date,
                    'game_id': play.match.game.game_id,
                    'game_name': play.match.game.name,
                    'did_win': play.did_win
                }, player.plays))
                }, players))}), 200
    elif request.method == 'POST':
        post_json = request.get_json()
        new_player = Player(first_name=post_json['first_name'], last_name=post_json['last_name'])
        db.session.add(new_player)
        db.session.commit()
        return jsonify({
            'player_id': new_player.player_id,
            'first_name': new_player.first_name,
            'last_name': new_player.last_name,
            'plays': list(map(lambda play: {
                    'play_id': play.play_id,
                    'match_id': play.match_id,
                    'match_date': play.match.date,
                    'game_id': play.match.game.game_id,
                    'game_name': play.match.game.name,
                    'did_win': play.did_win
                }, new_player.plays))
        }), 201

@app.route('/games/', methods=['GET', 'POST'])
@app.route('/games/<game_id>/')
def games(game_id=None):
    if request.method == 'GET':
        if game_id:
            game = Game.query.filter_by(game_id=game_id).first()
            return jsonify({'game_id': game.game_id, 'name': game.name}), 200
        else:
            games = Game.query.order_by(Game.game_id).all()
            return jsonify({'games': list(map(lambda game: {
                'game_id': game.game_id,
                'name': game.name
                }, games))}), 200
    elif request.method == 'POST':
        post_json = request.get_json()
        new_game = Game(name=post_json['name'])
        db.session.add(new_game)
        db.session.commit()
        return jsonify({
            'game_id': new_game.game_id,
            'name': new_game.name
        }), 201

@app.route('/matches/', methods=['GET', 'POST'])
@app.route('/matches/<match_id>/')
def matches(match_id=None):
    if request.method == 'GET':
        if match_id:
            match = Match.query.filter_by(match_id=match_id).first()
            return jsonify({
                'match_id': match.match_id,
                'match_date': match.date,
                'game_id': match.game.game_id,
                'game_name': match.game.name,
                'players': list(map(lambda play: {
                    'player_id': play.player_id,
                    'first_name': play.player.first_name,
                    'last_name': play.player.last_name,
                    'did_win': play.did_win
                }, match.plays))
            })
        else:
            matches = Match.query.order_by(Match.match_id).all()
            return jsonify({'matches':
                list(map(lambda match: {
                    'match_id': match.match_id,
                    'match_date': match.date,
                    'game_id': match.game.game_id,
                    'game_name': match.game.name,
                    'players': list(map(lambda play: {
                            'player_id': play.player_id,
                            'first_name': play.player.first_name,
                            'last_name': play.player.last_name,
                            'did_win': play.did_win
                        }, match.plays))
                }, matches))
            })
    elif request.method == 'POST':
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

        return jsonify({
            'match_id': new_match.match_id,
            'game_id': new_match.game_id,
            'game_name': new_match.game.name,
            'date': new_match.date,
            'players': list(map(lambda play: {
                    'player_id': play.player_id,
                    'first_name': play.player.first_name,
                    'last_name': play.player.last_name,
                    'did_win': play.did_win
                }, new_match.plays))
        }), 201
