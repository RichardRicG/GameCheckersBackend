import random
def get_all_computer_moves(board):
# function to get all valid moves for the computer playeing  as ('c' pieces).
    
    moves = []

    # Loop through each row and column of the board
    for row in range(8):
        for col in range(8):
            if board[row][col] == 'c':  # If we find a computer's piece ('c')
                # Check the four possible directions for a move
                if row > 0 and col > 0 and board[row - 1][col - 1] == ' ':
                    # Up-left move
                    moves.append((row, col, row - 1, col - 1))
                if row > 0 and col < 7 and board[row - 1][col + 1] == ' ':
                    # Up-right move
                    moves.append((row, col, row - 1, col + 1))
                if row < 7 and col > 0 and board[row + 1][col - 1] == ' ':
                    # Down-left move
                    moves.append((row, col, row + 1, col - 1))
                if row < 7 and col < 7 and board[row + 1][col + 1] == ' ':
                    # Down-right move
                    moves.append((row, col, row + 1, col + 1))

    return moves