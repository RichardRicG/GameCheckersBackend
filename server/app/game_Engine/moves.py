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