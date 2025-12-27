"""Core package for Xiangqi rules engine v1.0.0."""

from xiangqi_core.board import Board, Position, initial_position
from xiangqi_core.attack import find_king, is_in_check, is_square_attacked
from xiangqi_core.coord import Coord
from xiangqi_core.errors import (
    GameOverError,
    IllegalMoveError,
    ParseCoordError,
    ParseMoveError,
    XiangqiError,
)
from xiangqi_core.game import Game, GameResult
from xiangqi_core.legality import generate_legal_moves, is_checkmate, is_legal_move
from xiangqi_core.move import Move
from xiangqi_core.piece import Piece
from xiangqi_core.types import PieceType, Side
from xiangqi_core.rules import is_pseudo_legal_move

__all__ = [
    "Game",
    "GameResult",
    "Board",
    "Coord",
    "GameOverError",
    "generate_legal_moves",
    "find_king",
    "IllegalMoveError",
    "is_checkmate",
    "is_in_check",
    "is_legal_move",
    "is_pseudo_legal_move",
    "is_square_attacked",
    "Move",
    "ParseCoordError",
    "ParseMoveError",
    "Piece",
    "PieceType",
    "Position",
    "Side",
    "XiangqiError",
    "initial_position",
]
