from flask import Blueprint, request, jsonify
from .game_routes import CheckerGame
from .board import global_board

game_routes = Blueprint('game_routes', __name__)

# Initialize a game instance with the global board
game = CheckerGame(global_board.board)

@game_routes.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    start_pos = data.get('start_pos')  # list [x, y]
    end_pos = data.get('end_pos')      # list [x, y]
    player = data.get('player')        # Player piece, e.g., "p"

    if start_pos is None or end_pos is None or player is None:
        return jsonify({"success": False, "message": "Invalid input data"}), 400

    # Attempt to make the move
    success = game.make_move(start_pos, end_pos, player)

    if success:
        return jsonify({
            "success": True,
            "message": f"{player} moved from {start_pos} to {end_pos}",
            "board": game.get_board()
        })
    else:
        # Get possible moves for the piece at the start position
        possible_moves = game.get_possible_moves(start_pos, player)
        return jsonify({
            "success": False,
            "message": "Invalid move",
            "possible_moves": possible_moves
        }), 400