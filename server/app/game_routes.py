from flask import Blueprint, jsonify
from .board import global_board

main = Blueprint('main', __name__ )
board_bp = Blueprint('board', __name__)

@main.route('/')
def home():
    return "welcome grp4 checkers, testing!"

@board_bp.route('/board', methods=['GET'])
def get_board():
    return jsonify(global_board.board)

