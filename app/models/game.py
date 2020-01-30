from app import db


class Game(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    matches = db.relationship('Match', backref='game', lazy=True)
