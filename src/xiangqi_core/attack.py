"""Attack and check detection utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from xiangqi_core.board import Position
from xiangqi_core.coord import Coord
from xiangqi_core.move import Move
from xiangqi_core.rules import _count_blockers, is_pseudo_legal_move
from xiangqi_core.types import PieceType, Side

if TYPE_CHECKING:  # pragma: no cover - import cycle guard
    from xiangqi_core.game import Game


def find_king(position: Position, side: Side) -> Coord:
    """Return the coordinate of ``side``'s king."""

    for coord, piece in position.board:
        if piece.type is PieceType.KING and piece.side is side:
            return coord
    raise ValueError(f"No king found for side {side}")


def is_square_attacked(position: Position, by_side: Side, square: Coord) -> bool:
    """Return ``True`` if any piece of ``by_side`` attacks ``square``."""

    for coord, piece in position.board:
        if piece.side is not by_side:
            continue

        if piece.type is PieceType.KING and coord.x == square.x:
            if _count_blockers(position.board, coord, square) == 0:
                return True

        if is_pseudo_legal_move(position, Move(coord, square)):
            return True

    return False


def is_in_check(position: Position, side: Side) -> bool:
    """Return ``True`` if ``side``'s king is under attack."""

    king_square = find_king(position, side)
    return is_square_attacked(position, side.opponent(), king_square)
