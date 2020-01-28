from app import db

class Player(db.Model):
    __tablename__ = 'players'
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    plays = db.relationship('Play', backref='player', lazy=True)
