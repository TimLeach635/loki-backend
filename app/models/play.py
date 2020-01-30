from app import db


class Play(db.Model):
    __tablename__ = "plays"
    play_id = db.Column(db.Integer, primary_key=True, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.match_id"), nullable=False)
    player_id = db.Column(
        db.Integer, db.ForeignKey("players.player_id"), nullable=False
    )
    did_win = db.Column(db.Boolean, nullable=False)
