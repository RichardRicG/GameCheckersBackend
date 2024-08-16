# game_routes.py
from functools import wraps
from flask import Blueprint, g, jsonify, request
import jwt

from ..models import db, Player, Game
from ..game_Engine.board import global_board, create_initial_board  
# from flask_jwt_extended import jwt_required, get_jwt_identity
from ..game_Engine.computer import *



game_blueprint = Blueprint('game', __name__)


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
            g.user_data = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 403

        return f(*args, **kwargs)

    return decorated

# @main.route('/')
# def home():
#     return "Welcome GRP4 Checkers, testing!"

@game_blueprint.route('/board', methods=['GET'])
@token_required
def get_board():
    player_pieces, computer_pieces =count_pieces(global_board.board)
    game_winner = check_winner(global_board.board)

    if game_winner!=None:
        return jsonify({'message': f'Game over. {game_winner} wins!','Computer_Pieces':computer_pieces,'Player_pieces':player_pieces,'Game_Winner':game_winner, 'board': global_board.board}), 200
    elif game_winner ==None:
       return jsonify({'message': f'Game Ongoing','Computer_Pieces':computer_pieces,'Player_pieces':player_pieces,'Game_Winner':"Ongoing", 'board': global_board.board}), 200

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

                # Save the move to the database
                current_user = g.user_data
                current_player = Player.query.filter_by(username=current_user['username']).first()
                new_move = Game(
                    player_id=current_player.id,
                    board=board,
                    move_player='player',
                    start_row=start_row,
                    start_col=start_col,
                    end_row=end_row,
                    end_col=end_col
                )
                db.session.add(new_move)
                db.session.commit()


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

                         # Save the computer's move to the database
                        new_move_computer = Game(
                            player_id=current_player.id,
                            board=board,
                            move_player='computer',
                            start_row=computer_move_details['start'][0],
                            start_col=computer_move_details['start'][1],
                            end_row=computer_move_details['end'][0],
                            end_col=computer_move_details['end'][1]
                        )
                        db.session.add(new_move_computer)
                        db.session.commit()
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


@game_blueprint.route('/restore', methods=['GET'])
@token_required
def restore_game():
    current_user = g.user_data
    current_player = Player.query.filter_by(username=current_user['username']).first()

    # Fetch the last move from the Game table
    last_move = Game.query.filter_by(player_id=current_player.id).order_by(Game.id.desc()).first()

    if last_move:
        # Restore the board to the state of the last move
        global_board.board = last_move.board
        return jsonify({'message': 'Game restored to previous state', 'board': last_move.board}), 200
    else:
        return jsonify({'message': 'No previous moves found to restore.'}), 404


# Route for starting a new game
@game_blueprint.route("/new_game", methods=['GET'])
@token_required
def new_game():
    current_user = g.user_data()
    current_player = Player.query.filter_by(username=current_user['username']).first()

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


    
@game_blueprint.route('/quitgame', methods=['GET'])
@token_required
def quit_player():

    try:
        global_board.board = create_initial_board()
        game.board = global_board.board

        game_state['current_turn'] = 'player'
        
        db.session.commit()

        return jsonify({"message": "Game restarted", "board": game.board}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@game_blueprint.route('/restart', methods=['GET'])
@token_required
def restart_player():
    
    try:

        global_board.board = create_initial_board()
        game.board = global_board.board
        game_state['current_turn'] = 'player'
        db.session.commit()

        return jsonify({"message": "Game quitted", "board": game.board}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@game_blueprint.route('/logout', methods=['GET'])
@token_required
def logout_player():

    try:

        global_board.board = create_initial_board()
        game.board = global_board.board
        
        game_state['current_turn'] = 'player'
        db.session.commit()

        return jsonify({"message": "Game logout", "board": game.board}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

       
