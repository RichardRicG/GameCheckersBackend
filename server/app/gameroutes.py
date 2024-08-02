from flask import Flask, Blueprint, request, jsonify

app = Flask(__name__)

game_blueprint = Blueprint('game', __name__)

current_board = [
    [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
    ['c', ' ', 'c', ' ', 'c', ' ', 'c', ' '],
    [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' '],
    [' ', 'p', ' ', 'p', ' ', 'p', ' ', 'p'],
    ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' ']
]

@game_blueprint.route("/game", methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        # Get the game board, start and end positions from the request data
        board = request.json.get('board', current_board)  
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




























































































# from flask import Flask, Blueprint, request, jsonify

# app = Flask(__name__)

# game_blueprint = Blueprint('game', __name__)

# current_board = [
#       [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
#       ['c', ' ', 'c', ' ', 'c', ' ', 'c', ' '],
#       [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
#       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#       ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' '],
#       [' ', 'p', ' ', 'p', ' ', 'p', ' ', 'p'],
#       ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' ']
# ]

# @game_blueprint.route("/game", methods=['GET', 'POST'])
# def game():
#     if request.method == 'POST':
#         # Get the game board, start and end positions from the request data
#         board = request.json.get('board')
#         start_row = request.json.get('start_row')
#         start_col = request.json.get('start_col')
#         end_row = request.json.get('end_row')
#         end_col = request.json.get('end_col')

#         if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
#             return jsonify({'message': 'Invalid move. Out of board bounds.'}), 400

#         if abs(start_row - end_row) != 1 or abs(start_col - end_col) != 1:
#             return jsonify({'message': 'Invalid move. Must be diagonal.'}), 400

#         # captured_piece = None

#         # Check if the move is valid
# def is_valid_move(board, start_row, start_col, end_row, end_col):        
#         if board[start_row][start_col] == 'p' and end_row < start_row:
#             return jsonify({'message': 'Invalid move. Player cannot move backwards.'}), 400
#         elif board[start_row][start_col] == 'c' and end_row > start_row:
#             return jsonify({'message': 'Invalid move. Player cannot move backwards.'}), 400

#         if board[start_row][start_col] in ('p', 'c'):
#             captured_piece = board[end_row][end_col]
#             board[end_row][end_col] = board[start_row][start_col]
#             board[start_row][start_col] =' '

#         if is_valid_move(board, start_row, start_col, end_row, end_col):
#             if captured_piece == 'p':
#                 board[end_row]

#         if is_valid_move(board, start_row, start_col, end_row, end_col):

#              if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
#                  if board[end_row][end_col] == ' ':
#                       return False
#         elif abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
#             captured_row = (start_row + end_row) // 2
#             captured_col = (start_col + end_col) // 2
#             if board[captured_row][captured_col] in ('p', 'c'):
#                 return True
#         return False


            












































    # return jsonify({'board': board, 'status': 'Game in progress'})
    #     else:
    #         return jsonify({'error': 'Invalid move'}), 400

    # elif request.method == 'GET':
    #     # Return the current game state
    #     return jsonify({'board': current_board, 'status': 'Game in progress'})

# def is_valid_move(board, start_row, start_col, end_row, end_col):
    # if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
    #     if board[end_row][end_col] == ' ':
    #         return False
    # elif abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
    #     captured_row = (start_row + end_row) // 2
    #     captured_col = (start_col + end_col) // 2
    #     if board[captured_row][captured_col] in ('p', 'c'):
    #         return True
    # return False



