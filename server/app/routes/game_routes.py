from flask import Blueprint, jsonify, request
from ..game_Engine.board import global_board
from ..game_Engine.computer import get_all_computer_moves

main = Blueprint('main', __name__ )
board_bp = Blueprint('board', __name__)
game_blueprint = Blueprint('game', __name__)

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

        is_valid, error_message = is_valid_move(board, start_row, start_col, end_row, end_col)

        if is_valid:
            # Update the board for a valid move
            board[end_row][end_col] = board[start_row][start_col]
            board[start_row][start_col] = ' '
            return jsonify({'message': 'Valid move', 'board': board})
        else:
            return jsonify({'message': error_message}), 400

    return jsonify({'message': 'Invalid request method'}), 405



def is_valid_move(board, start_row, start_col, end_row, end_col):
    piece = board[start_row][start_col]
    
    if piece == ' ':
        return False, 'Invalid move. No piece at the starting position.'
    
    if piece == 'p' and end_row >= start_row:
        return False, 'Invalid move. Player cannot move backwards.'
    elif piece == 'c' and end_row <= start_row:
        return False, 'Invalid move. Computer cannot move backwards.'
    
    # Check if the end position is empty and the move is diagonal
    if board[end_row][end_col] == ' ':
        if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
            return True, None
        elif abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
            captured_row = (start_row + end_row) // 2
            captured_col = (start_col + end_col) // 2
            if board[captured_row][captured_col] in ('p', 'c'):
                return True, None
    
    return False, 'Invalid move.'

#routes for the computer 
@game_blueprint.route("/computer_move", methods=['POST'])
def computer_move():
    # Make a random move for the computer
    computer_move_details = get_all_computer_moves(global_board.board)
#
    if computer_move_details:
        return jsonify({
            'message': 'Computer made a move',
            'computer_move': computer_move_details,
            'board': global_board.board
        })
    else:
        return jsonify({'message': 'No valid moves available for the computer'}), 400