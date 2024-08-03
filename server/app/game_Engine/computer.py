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
def make_computer_move(board):
    
    #Function to make a random move for the computer. computer playoing as
    possible_moves = get_all_computer_moves(board)
#if we have no move for computer, such as cannot move any more or game is over 
    if not possible_moves:
        print("No valid moves available for the computer.")
        return None
#random moves for the computer getting possible moves from function get all possible moves
    move = random.choice(possible_moves)
    start_row, start_col, end_row, end_col = move

    # Update the board with the computer's move
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = ' '  # Clear the starting position

    # Print the move and the updated board state
    print(f"Computer moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")

#return the current move state 
    return {'start': (start_row, start_col), 'end': (end_row, end_col)}
