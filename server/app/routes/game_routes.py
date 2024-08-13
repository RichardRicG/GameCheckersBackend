from flask import Blueprint, g, jsonify, request
from ..models import db, Player, Game
from ..game_Engine.board import global_board, create_initial_board  
from ..game_Engine.computer import *
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from functools import wraps

from flask_cors import CORS

game_blueprint = Blueprint('game', __name__)

cors = CORS()
# Initialize 
game_state = {
    'current_turn': 'player',
}

# JWT authentication decorator using Flask-JWT-Extended
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            g.current_user = current_user
        except Exception as e:
            return jsonify({'message': str(e)}), 403
        
        return f(*args, **kwargs)
    return decorated

@game_blueprint.route('/board', methods=['GET'])
@token_required
def get_board():
    return jsonify(global_board.board)

@game_blueprint.route("/game", methods=['POST'])
@token_required
def game():
    if request.method == 'POST':
        board = request.json.get('board', global_board.board)
        start_row = request.json.get('start_row')
        start_col = request.json.get('start_col')
        end_row = request.json.get('end_row')
        end_col = request.json.get('end_col')

        # Ensure the move coordinates are within bounds
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return jsonify({'message': 'Invalid move. Out of board bounds.'}), 400

        if game_state['current_turn'] == 'player':
            
            move_successful, is_capture, more_captures = make_player_move(board, start_row, start_col, end_row, end_col)

            if move_successful:
                if is_capture and more_captures:
                    return jsonify({
                        'message': 'Capture successful. Continue capturing with the same piece.',
                        'board': board
                    })
                else:
                    # Change turn to computer
                    game_state['current_turn'] = 'computer'

                    # Computer's move
                    computer_move_details = make_computer_move(board)
                    if computer_move_details:
                        # Check for a winner after the computer's move
                        winner = check_winner(board)
                        if winner:
                            return jsonify({'message': f'{winner} wins!', 'board': board})

                        # Change turn back to player
                        game_state['current_turn'] = 'player'
                        return jsonify({
                            'message': 'Valid move',
                            'player_move': {'start': (start_row, start_col), 'end': (end_row, end_col)},
                            'computer_move': computer_move_details,
                            'board': board
                        })
                    else:
                        return jsonify({'message': 'No valid moves available for the computer', 'board': board}), 400

            else:
                return jsonify({'message': 'Invalid move'}), 400

        elif game_state['current_turn'] == 'computer':
            # Handle the computer's move
            computer_move_details = make_computer_move(board)
            if computer_move_details:
                # Check for a winner after the computer's move
                winner = check_winner(board)
                if winner:
                    return jsonify({'message': f'{winner} wins!', 'board': board})

                # Change turn back to player
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
@jwt_required()
def new_game():
    current_user = get_jwt_identity()
    current_player = Player.query.filter_by(id=current_user['user_id']).first()

    if current_player:
        try:
            # Reset the board to the initial state for new game
            global_board.board = create_initial_board()
            new_game = Game(player_id=current_player.id, board=global_board.board)
            db.session.add(new_game)
            db.session.commit()
            return jsonify({'message': 'New game started', 'board': new_game.board}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        return jsonify({'message': 'User not logged in'}), 401
