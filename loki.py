import time

from app import app
from app import db
from app.models.player import Player
from app.models.game import Game
from app.models.match import Match
from app.models.play import Play

# try to connect to the database
retries = 5
while True:
    try:
        db.create_all()
        break
    except Exception as exc:
        if retries == 0:
            raise exc
        retries -= 1
        print("Failed to connect to database.\nRetries remaining:", retries)
        time.sleep(5)
