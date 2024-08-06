import random

def get_all_computer_captures(board):
    """
    Get all valid capture moves for the computer playing as 'c' pieces.
    """
    captures = []

    for row in range(8):
        for col in range(8):
            if board[row][col] == 'c':  # If we find a computer's piece ('c')
                # Check for captures (jumps)
                if row > 1 and col > 1 and board[row - 1][col - 1].lower() == 'p' and board[row - 2][col - 2] == ' ':
                    # Up-left capture
                    captures.append((row, col, row - 2, col - 2, row - 1, col - 1))
                if row > 1 and col < 6 and board[row - 1][col + 1].lower() == 'p' and board[row - 2][col + 2] == ' ':
                    # Up-right capture
                    captures.append((row, col, row - 2, col + 2, row - 1, col + 1))
                if row < 6 and col > 1 and board[row + 1][col - 1].lower() == 'p' and board[row + 2][col - 2] == ' ':
                    # Down-left capture
                    captures.append((row, col, row + 2, col - 2, row + 1, col - 1))
                if row < 6 and col < 6 and board[row + 1][col + 1].lower() == 'p' and board[row + 2][col + 2] == ' ':
                    # Down-right capture
                    captures.append((row, col, row + 2, col + 2, row + 1, col + 1))

    return captures

def get_all_computer_moves(board):
    """
    Get all valid moves for the computer playing as 'c' pieces, including normal moves.
    """
    moves = []
    captures = get_all_computer_captures(board)  # Get all capture moves

    if captures:
        return captures  # Prioritize capture moves if available

    # Check for normal moves if no captures are available
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
    """
    Function to make a move for the computer, with captures prioritized if available.
    """
    possible_moves = get_all_computer_moves(board)

    if not possible_moves:
        print("No valid moves available for the computer.")
        return None

    move = random.choice(possible_moves)
    
    if len(move) == 5:  # This is a capture move
        start_row, start_col, end_row, end_col, capture_row, capture_col = move
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = ' '
        board[capture_row][capture_col] = ' '  # Remove the captured piece
        print(f"Computer captured a piece at ({capture_row}, {capture_col}) and moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    else:  # Normal move
        start_row, start_col, end_row, end_col = move
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = ' '  # Clear the starting position
        print(f"Computer moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    
    print_board(board)
    return {'start': (start_row, start_col), 'end': (end_row, end_col)}

def is_valid_position(row, col, board):
    """
    Checks if a position is within bounds and empty.
    """
    if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == ' ':
        return True
    return False

def print_board(board):
    """
    Prints the current state of the board in a readable format.
    """
    print("Current Board State:")
    for row in board:
        print(' '.join(row))
    print("\n")
