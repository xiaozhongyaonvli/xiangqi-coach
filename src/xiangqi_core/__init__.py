"""Core package for Xiangqi rules engine v1.0.0."""

from xiangqi_core.board import Board, Position, initial_position
from xiangqi_core.coord import Coord
from xiangqi_core.errors import (
    GameOverError,
    IllegalMoveError,
    ParseCoordError,
    ParseMoveError,
    XiangqiError,
)
from xiangqi_core.move import Move
from xiangqi_core.piece import Piece
from xiangqi_core.types import PieceType, Side

__all__ = [
    "Board",
    "Coord",
    "GameOverError",
    "IllegalMoveError",
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
