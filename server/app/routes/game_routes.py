from flask import Blueprint, jsonify, request, g as globaluserdata
from ..models import db, Player, Game
from ..game_Engine.board import global_board, create_initial_board  

from ..game_Engine.computer import *
from functools import wraps

import jwt

from flask_cors import CORS


main = Blueprint('main', __name__)
game_blueprint = Blueprint('game', __name__)

cors = CORS()
SECRET_KEY = 'GRP4_Checkers'

# Initialize 
game_state = {
    'current_turn': 'player',
}
# JWT authentiction decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            token = token.split()[1]  
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            globaluserdata.current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 403

        return f(*args, **kwargs)

    return decorated

@main.route('/')
def home():
    return "Welcome GRP4 Checkers, testing!"

@game_blueprint.route('/board', methods=['GET'])
@token_required
def get_board():
    return jsonify(global_board.board)
@game_blueprint.route("/game", methods=['POST'])
@token_required
def game():
    if request.method == 'POST':
        # Get the game board, start and end positions from the request data
        board = request.json.get('board', global_board.board)
        start_row = request.json.get('start_row')
        start_col = request.json.get('start_col')
        end_row = request.json.get('end_row')
        end_col = request.json.get('end_col')

        # Validate move within board boundaries
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return jsonify({'message': 'Invalid move. Out of board bounds.'}), 400

        if game_state['current_turn'] == 'player':
            # Handle the player's move
            is_valid, error_message = is_valid_move(board, start_row, start_col, end_row, end_col)

            if is_valid:
                # Execute the player's move
                board[end_row][end_col] = board[start_row][start_col]
                board[start_row][start_col] = ' '

                # Promote to king if necessary
                crown_piece(board, end_row, end_col)

                # Check for a winner after the player's move
                winner = check_winner(board)
                if winner:
                    return jsonify({'message': f'{winner} wins!', 'board': board})

                # Change the turn to computer
                game_state['current_turn'] = 'computer'

                # Computer's move
                computer_move_details = make_computer_move(board)

                if computer_move_details:
                    # Check for a winner after computer's move
                    winner = check_winner(board)
                    if winner:
                        return jsonify({'message': f'{winner} wins!', 'board': board})

                    # Change the turn back to player
                    game_state['current_turn'] = 'player'
                else:
                    return jsonify({'message': 'No valid moves available for the computer', 'board': board}), 400

                return jsonify({
                    'message': 'Valid move',
                    'player_move': {'start': (start_row, start_col), 'end': (end_row, end_col)},
                    'computer_move': computer_move_details,
                    'board': board
                })
            else:
                return jsonify({'message': error_message}), 400

        elif game_state['current_turn'] == 'computer':
            # Handle the computer's move if the computer's turn is invoked directly
            computer_move_details = make_computer_move(board)

            if computer_move_details:
                # Check for a winner after computer's move
                winner = check_winner(board)
                if winner:
                    return jsonify({'message': f'{winner} wins!', 'board': board})

                # Change the turn back to player
                game_state['current_turn'] = 'player'
                return jsonify({
                    'message': 'Computer made a move',
                    'computer_move': computer_move_details,
                    'board': board
                })
            else:
                return jsonify({'message': 'No valid moves available for the computer'}), 400

        else:
            return jsonify({'message': 'It\'s not your turn. Wait for the computer to make a move.'}), 403

    return jsonify({'message': 'Invalid request method'}), 405

# Route for starting a new game
@game_blueprint.route("/newgame", methods=['GET'])
@token_required
def new_game():
    current_player = Player.query.filter_by(username=globaluserdata.current_user['username']).first()

    if current_player:
        try:
            # ResEt the board to the initial state for new game
            global_board.board = create_initial_board()
            new_game = Game(player_id=current_player.id, board=global_board.board)
            db.session.add(new_game)
            db.session.commit()
            return jsonify({'message': 'New game started', 'board': new_game.board}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        return jsonify({'message': 'User not logged in'}), 401
    


