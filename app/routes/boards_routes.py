from app import db
from app.models.board import Board
from app.models.card import Card
from .board_routes_helper import validate_model, validate_attribute, validate_board
from flask import Blueprint, jsonify, make_response, request, abort



board_bp = Blueprint("boards", __name__, url_prefix="/boards")

@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    validate_board(request_body)
    new_board = Board.from_dict(request_body)
    db.session.add(new_board)
    db.session.commit()
    return new_board.to_dict(), 201

@board_bp.route("", methods=["GET"])
def get_boards():
    boards = []
    board_query = Board.query.all()

    for board in board_query:
        boards.append(board.to_dict())
    return jsonify(boards)

@board_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    board = validate_model(Board, board_id)
    if not board.status:
        abort(make_response({"details": "This board is archived"}, 400))
    return board.to_dict(), 201

@board_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    validate_board(request_body)
    board.title = request_body["title"]
    board.owner = request_body["owner"]
    db.session.commit()
    db.session.refresh(board)
    return board.to_dict()

"""
currently not working, will test again when i pull card models
@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)
    # if a board is deleted, this board and its associated cards will be archived
    cards = board.cards.query.all()
    for card in cards:
        card.status = False
    board.status = False
    db.session.commit()
    return board.to_dict(), 200
"""
@board_bp.route("/<board_id>", methods=["PATCH"])
def patch_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    board = validate_attribute(board, request_body)
    db.session.commit()
    db.session.refresh(board)
    return board.to_dict()