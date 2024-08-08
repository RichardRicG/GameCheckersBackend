import random

def get_all_captures(board, piece_type):
    """
    Get all valid capture moves for the given piece type ('c' for computer, 'p' for player).
    """
    captures = []
    directions = {
        'p': [(-2, -2), (-2, 2)],
        'c': [(2, -2), (2, 2)],
        'P': [(-2, -2), (-2, 2), (2, -2), (2, 2)],
        'C': [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    }
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.lower() == piece_type:
                for dr, dc in directions[piece]:
                    mid_row, mid_col = row + dr // 2, col + dc // 2
                    end_row, end_col = row + dr, col + dc
                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        if board[mid_row][mid_col].lower() in ('p', 'c') and board[mid_row][mid_col].lower() != piece_type and board[end_row][end_col] == ' ':
                            captures.append((row, col, end_row, end_col, mid_row, mid_col))
    return captures

def get_all_moves(board, piece_type):
    """
    Get all valid moves for the given piece type ('c' for computer, 'p' for player), including normal moves.
    """
    moves = []
    directions = {
        'p': [(-1, -1), (-1, 1)],
        'c': [(1, -1), (1, 1)],
        'P': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        'C': [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    }
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.lower() == piece_type:
                for dr, dc in directions[piece]:
                    end_row, end_col = row + dr, col + dc
                    if 0 <= end_row < 8 and 0 <= end_col < 8 and board[end_row][end_col] == ' ':
                        moves.append((row, col, end_row, end_col))
    return moves

def count_pieces(board, piece_type):
    """
    Counts the number of pieces of a given type on the board.
    """
    count = 0
    for row in board:
        count += row.count(piece_type.lower())
        count += row.count(piece_type.upper())
    return count

def make_computer_move(board):
    """
    Function to make a move for the computer, prioritizing captures over normal moves.
    """
    capture_moves = get_all_captures(board, 'c')
    possible_moves = get_all_moves(board, 'c')

    if capture_moves:
        move = random.choice(capture_moves)
        start_row, start_col, end_row, end_col, capture_row, capture_col = move
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = ' '
        board[capture_row][capture_col] = ' '  # Remove the captured piece
        print(f"Computer captured a piece at ({capture_row}, {capture_col}) and moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    elif possible_moves:
        move = random.choice(possible_moves)
        start_row, start_col, end_row, end_col = move
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = ' '  # Clear the starting position
        print(f"Computer moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    else:
        print("No valid moves available for the computer.")
        return None

    # Promote to king if necessary
    if end_row == 7 and board[end_row][end_col] == 'c':
        board[end_row][end_col] = 'C'

    print_board(board)

    return {'start': (start_row, start_col), 'end': (end_row, end_col)}

def make_player_move(board, start_row, start_col, end_row, end_col):
    """
    Function to make a move for the player, enforcing captures over normal moves.
    """
    capture_moves = get_all_captures(board, 'p')
    if capture_moves:
        # If there are capture moves available, player must make a capture
        valid_move = False
        for move in capture_moves:
            if move[0] == start_row and move[1] == start_col and move[2] == end_row and move[3] == end_col:
                valid_move = True
                capture_row, capture_col = move[4], move[5]
                board[end_row][end_col] = board[start_row][start_col]
                board[start_row][start_col] = ' '
                board[capture_row][capture_col] = ' '  # Remove the captured piece
                print(f"Player captured a piece at ({capture_row}, {capture_col}) and moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
                break
        if not valid_move:
            print("Invalid move. You must capture an opponent's piece.")
            return False
    else:
        valid, message = is_valid_move(board, start_row, start_col, end_row, end_col)
        if valid:
            board[end_row][end_col] = board[start_row][start_col]
            board[start_row][start_col] = ' '
            print(f"Player moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
        else:
            print(message)
            return False

    # Promote to king if necessary
    if end_row == 0 and board[end_row][end_col] == 'p':
        board[end_row][end_col] = 'P'
        print("Player has promoted to a king.")
    
    print_board(board)

    return True

def is_valid_position(row, col, board):
    """
    Checks if a position is within bounds and empty.
    """
    return 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == ' '

def print_board(board):
    """
    Prints the current state of the board in a readable format.
    """
    print("Current Board State:")
    for row in board:
        print(' '.join(row))
    print("\n")

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
            if board[captured_row][captured_col].lower() in ('p', 'c'):
                captured_piece = board[captured_row][captured_col]
                board[captured_row][captured_col] = ' ' 
                return True, f'Captured {captured_piece}'
    
    return False, 'Invalid move.'


