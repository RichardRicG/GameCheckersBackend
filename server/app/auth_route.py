from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from .models import db, Player

auth_blueprint = Blueprint('auth_route', __name__)
bcrypt = Bcrypt()

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username:
        return jsonify({'message': 'Username is required.'}), 400
    if not email:
        return jsonify({'message': 'Email is required.'}), 400
    if not password:
        return jsonify({'message': 'Password is required.'}), 400

    if len(email) < 4:
        return jsonify({'message': 'Email is too short. Must be at least 4 characters.'}), 400
    if len(username) < 4:
        return jsonify({'message': 'Username is too short. Must be at least 4 characters.'}), 400
    if len(password) < 6:
        return jsonify({'message': 'Password is too short. Must be at least 6 characters.'}), 400

    existing_user = Player.query.filter_by(username=username).first()
    existing_email = Player.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({'message': 'Username already in use. Please choose a different one.'}), 409
    elif existing_email:
        return jsonify({'message': 'Email address already registered. Please use a different email.'}), 409
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_player = Player(username=username, email=email, password=hashed_password)
        db.session.add(new_player)
        db.session.commit()
        return jsonify({'message': 'Account created successfully!'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    player = Player.query.filter_by(username=username).first()

    if player and bcrypt.check_password_hash(player.password, password):
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Login unsuccessful. Please check your username and password.'}), 401
        
        