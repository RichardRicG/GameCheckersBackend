from flask import Blueprint, jsonify

def create_initial_board():
    return [
        [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
        ['c', ' ', 'c', ' ', 'c', ' ', 'c', ' '],
        [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' '],
        [' ', 'p', ' ', 'p', ' ', 'p', ' ', 'p'],
        ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' ']
    ]

class Board:
    def __init__(self):
        self.board = create_initial_board()

# Create a global board instance
global_board = Board()

board_bp = Blueprint('board', __name__)

@board_bp.route('/board', methods=['GET'])
def get_board():
    return jsonify(global_board.board)
