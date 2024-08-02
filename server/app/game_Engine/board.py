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

# Create a global board
global_board = Board()

