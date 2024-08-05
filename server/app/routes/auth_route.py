from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from ..models import db, Player
import jwt
import datetime

auth_blueprint = Blueprint('auth_route', __name__)
bcrypt = Bcrypt()
SECRET_KEY = 'GRP4_Checkers' 

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
        try:
            token = jwt.encode(
                {
                    'username': player.username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                },
                SECRET_KEY,
                algorithm='HS256'
            )

            # token  decoded to string 
            token = token.decode('utf-8') if isinstance(token, bytes) else token

            return jsonify({'message': 'Login successful!', 'token': token}), 200
        except Exception as e:
            return jsonify({'message': 'Token generation failed', 'error': str(e)}), 500
    else:
        return jsonify({'message': 'Login unsuccessful. Please check your username and password.'}), 401

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    # Logic for logout (if needed)
    return jsonify({'message': 'Logout endpoint'})

