
import random

def print_board(board):
    # Prints the current state of the board in a readable format.
    print("Current Board State:")
    for row in board:
        print(' '.join(row))
           # Print board, possible moves, and piece counts
    # print_board(board)
    print_possible_moves(board, 'p')
    player_count, computer_count = count_pieces(board)
    print(f"Player pieces: {player_count}, Computer pieces: {computer_count}")



def is_valid_position(row, col, board):
    # Checks if a position is within bounds and empty.
    return 0 <= row < len(board) and 0 <= col < len(board) and board[row][col] == ' '

def get_all_captures(board, piece_type):
    # Getting all valid capture moves for the piece type ('c' for computer, 'p' for player).
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
                        if board[mid_row][mid_col] != ' ' and board[end_row][end_col] == ' ':
                            # Check if the piece being captured is an opponent's piece
                            if board[mid_row][mid_col].lower() != piece_type:
                                captures.append((row, col, end_row, end_col, mid_row, mid_col))
    return captures

def get_all_moves(board, piece_type):
    # Get all valid moves for the given piece type ('c' for computer, 'p' for player), including normal moves.
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

def make_computer_move(board):
    # Function to make a move for the computer, prioritizing captures over normal moves.
    capture_moves = get_all_captures(board, 'c')
    possible_moves = get_all_moves(board, 'c')

    while capture_moves:
        move = random.choice(capture_moves)
        start_row, start_col, end_row, end_col, capture_row, capture_col = move
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = ' '
        board[capture_row][capture_col] = ' '
        print(f"Computer captured a piece at ({capture_row}, {capture_col}) and moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")

        # Check if further captures are possible for the same piece
        capture_moves = get_all_captures(board, 'c')
        # Narrow down to only those captures that involve the same piece
        capture_moves = [capture for capture in capture_moves if capture[0] == end_row and capture[1] == end_col]

        # Promote to king if necessary
        crown_piece(board, end_row, end_col)

        # Print the board after each capture
        print_board(board)

        # Check for winner after each capture
        winner = check_winner(board)
        if winner:
            print(f"Game over! {winner} wins!")
            return None

    if not capture_moves and possible_moves:
        # If no more captures are possible, make a normal move
        move = random.choice(possible_moves)
        start_row, start_col, end_row, end_col = move
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = ' '
        print(f"Computer moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
        
        # Promote to king if necessary
        crown_piece(board, end_row, end_col)

        print_board(board)

        # Check for winner after the normal move
        winner = check_winner(board)
        if winner:
            print(f"Game over! {winner} wins!")
            return None

    # Return the final move details
    return {'start': (start_row, start_col), 'end': (end_row, end_col)}
def make_player_move(board, start_row, start_col, end_row, end_col):
    capture_moves = get_all_captures(board, 'p')
    is_capture = False

    if capture_moves:
        valid_move = False
        for move in capture_moves:
            if move[0] == start_row and move[1] == start_col and move[2] == end_row and move[3] == end_col:
                valid_move = True
                is_capture = True
                capture_row, capture_col = move[4], move[5]
                board[end_row][end_col] = board[start_row][start_col]
                board[start_row][start_col] = ' '
                board[capture_row][capture_col] = ' '
                print(f"Player captured a piece at ({capture_row}, {capture_col}) and moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
                break
        if not valid_move:
            print("Invalid move. You must capture an opponent's piece.")
            return False, False
    else:
        valid, message = is_valid_move(board, start_row, start_col, end_row, end_col)
        if valid:
            board[end_row][end_col] = board[start_row][start_col]
            board[start_row][start_col] = ' '
            print(f"Player moved from ({start_row}, {start_col}) to ({end_row}, {end_col})")
        else:
            print(message)
            return False, False

    # Promote to king if necessary
    crown_piece(board, end_row, end_col)
    
 
    # Check for winner
    winner = check_winner(board)
    if winner:
        print(f"Game over! {winner} wins!")
        return False

    return True, is_capture

#for all possible move p can make 
def print_possible_moves(board, piece_type):
    # Print all possible moves for the given piece type ('p' for player).
    moves = get_all_moves(board, piece_type)
    captures = get_all_captures(board, piece_type)
    all_moves = moves + captures
    
    if all_moves:
        print(f"Possible moves for {piece_type.upper()}:")
        for move in all_moves:
            if len(move) == 4:  # Regular move
                start_row, start_col, end_row, end_col = move
                print(f"Move from ({start_row}, {start_col}) to ({end_row}, {end_col})")
            elif len(move) == 6:  # Capture move
                start_row, start_col, end_row, end_col, capture_row, capture_col = move
                print(f"Capture move from ({start_row}, {start_col}) to ({end_row}, {end_col}) capturing ({capture_row}, {capture_col})")
    else:
        print(f"No possible moves for {piece_type.upper()}.")

def count_pieces(board):
    # Counts the number of pieces for both player and computer on the board.
    # Returns a tuple with the counts (player_pieces, computer_pieces).
    player_pieces = 0
    computer_pieces = 0

    for row in board:
        player_pieces += row.count('p') + row.count('P')
        computer_pieces += row.count('c') + row.count('C')
    
    return player_pieces, computer_pieces

def crown_piece(board, row, col):
    # Promotes a piece to a king if it reaches the opposite end of the board.
    piece = board[row][col]
    if piece == 'p' and row == 0:
        board[row][col] = 'P'
        print(f"Player's piece at ({row}, {col}) promoted to a king (P).")
    elif piece == 'c' and row == 7:
        board[row][col] = 'C'
        print(f"Computer's piece at ({row}, {col}) promoted to a king (C).")


def is_valid_move(board, start_row, start_col, end_row, end_col, capture=False):
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

def check_winner(board):
    # Check if there is a winner based on the remaining pieces or available moves.
    player_pieces, computer_pieces = count_pieces(board)

    if player_pieces == 0:
        return "Computer"
    elif computer_pieces == 0:
        return "Player"
    
    player_moves = get_all_moves(board, 'p') + get_all_captures(board, 'p')
    computer_moves = get_all_moves(board, 'c') + get_all_captures(board, 'c')

    if not player_moves:
        return "Computer"
    elif not computer_moves:
        return "Player"
    
    return None