from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # R/ship to Game
    games = db.relationship('Game', backref='player', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    board = db.Column(db.JSON, nullable=False)

    
class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    start_row = db.Column(db.Integer, nullable=False)
    start_col = db.Column(db.Integer, nullable=False)
    end_row = db.Column(db.Integer, nullable=False)
    end_col = db.Column(db.Integer, nullable=False)
    game = db.relationship('Game', backref=db.backref('moves', lazy=True))
    player = db.relationship('Player', backref=db.backref('moves', lazy=True))