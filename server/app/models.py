from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    # One-to-one relationship with Game
    game = db.relationship('Game', backref='player', lazy=True, uselist=False)  # uselist=False for one-to-one relationship

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to Player
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    
    # Board state
    board = db.Column(db.JSON, nullable=False)
    
    # Move-related fields
    move_player = db.Column(db.String(10), nullable=False)  # 'player' or 'computer'
    start_row = db.Column(db.Integer, nullable=False)
    start_col = db.Column(db.Integer, nullable=False)
    end_row = db.Column(db.Integer, nullable=False)
    end_col = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())