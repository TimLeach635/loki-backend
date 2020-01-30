def player_dict(player):
    return {
        "player_id": player.player_id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "plays": list(
            map(
                lambda play: {
                    "play_id": play.play_id,
                    "match_id": play.match_id,
                    "match_date": play.match.date,
                    "game_id": play.match.game.game_id,
                    "game_name": play.match.game.name,
                    "did_win": play.did_win,
                },
                player.plays,
            )
        ),
    }


def game_dict(game):
    return {"game_id": game.game_id, "name": game.name}


def match_dict(match):
    return {
        "match_id": match.match_id,
        "match_date": match.date,
        "game_id": match.game.game_id,
        "game_name": match.game.name,
        "players": list(
            map(
                lambda play: {
                    "player_id": play.player_id,
                    "first_name": play.player.first_name,
                    "last_name": play.player.last_name,
                    "did_win": play.did_win,
                },
                match.plays,
            )
        ),
    }
