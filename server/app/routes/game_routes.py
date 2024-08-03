from flask import Blueprint, jsonify, request
from ..game_Engine.board import global_board
from ..game_Engine.moves import is_valid_move
from ..game_Engine.computer import make_computer_move

main = Blueprint('main', __name__)
board_bp = Blueprint('board', __name__)
game_blueprint = Blueprint('game', __name__)

# to Initialize the game state
game_state = {
     # ' the player' or 'thr computer'
    'current_turn': 'player', 
}

@main.route('/')
def home():
    return "welcome grp4 checkers, testing!"

@board_bp.route('/board', methods=['GET'])
def get_board():
    return jsonify(global_board.board)

@game_blueprint.route("/game", methods=['POST'])
def game():
    if request.method == 'POST':
        # Get the game board, start and end positions from the request data
        board = request.json.get('board', global_board.board)  
        start_row = request.json.get('start_row')
        start_col = request.json.get('start_col')
        end_row = request.json.get('end_row')
        end_col = request.json.get('end_col')

        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return jsonify({'message': 'Invalid move. Out of board bounds.'}), 400

        if game_state['current_turn'] == 'player':
            is_valid, error_message = is_valid_move(board, start_row, start_col, end_row, end_col)

            if is_valid:
                # Update the board for a valid move
                board[end_row][end_col] = board[start_row][start_col]
                board[start_row][start_col] = ' '

                # Changing  the turn play to computer
                game_state['current_turn'] = 'computer'

                # now  a computer move random or mmediately after the player has made amove
                computer_move_details = make_computer_move(board)
                
                if computer_move_details:
                    # Change the turn back to player
                    game_state['current_turn'] = 'player'  

                return jsonify({
                    'message': 'Valid move',
                    'player_move': {'start': (start_row, start_col), 'end': (end_row, end_col)},
                    'computer_move': computer_move_details,
                    'board': board
                })
            else:
                return jsonify({'message': error_message}), 400
        else:
            return jsonify({'message': 'It\'s not your turn. Wait for the computer to make a move.'}), 403

    return jsonify({'message': 'Invalid request method'}), 405

# Routes for the computer
@game_blueprint.route("/computer_move", methods=['POST'])
def computer_move():
    if game_state['current_turn'] == 'computer':
        # Make a random move for the computer
        computer_move_details = make_computer_move(global_board.board)
        
        if computer_move_details:
            # Change the turn back to player
            game_state['current_turn'] = 'player'  
            return jsonify({
                'message': 'Computer made a move',
                'computer_move': computer_move_details,
                'board': global_board.board
            })
        else:
            return jsonify({'message': 'No valid moves available for the computer'}), 400
    else:
        return jsonify({'message': 'It\'s not the computer\'s turn.'}), 403
