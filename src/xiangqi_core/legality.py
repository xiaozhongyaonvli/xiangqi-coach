"""Full move legality checks including king safety."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from xiangqi_core.attack import is_in_check
from xiangqi_core.board import Board, Position
from xiangqi_core.coord import Coord
from xiangqi_core.move import Move
from xiangqi_core.rules import is_pseudo_legal_move
from xiangqi_core.types import Side

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from xiangqi_core.game import Game


def is_legal_move(game: "Game", move: Move) -> bool:
    """Return ``True`` if ``move`` is legal in ``game``'s current position."""

    position = game.position
    piece = position.board.get(move.frm)
    if piece is None or piece.side is not position.side_to_move:
        return False

    if not is_pseudo_legal_move(position, move):
        return False

    next_position = _apply_move(position, move)
    return not is_in_check(next_position, piece.side)


def generate_legal_moves(position: Position, side: Side) -> List[Move]:
    """Enumerate all legal moves for ``side`` in ``position``."""

    legal_moves: List[Move] = []
    for coord, piece in position.board:
        if piece.side is not side:
            continue
        for x in range(9):
            for y in range(10):
                dest = Coord(x, y)
                move = Move(coord, dest)
                if not is_pseudo_legal_move(position, move):
                    continue
                next_position = _apply_move(position, move, next_to_move=side.opponent())
                if is_in_check(next_position, side):
                    continue
                legal_moves.append(move)
    return legal_moves


def is_checkmate(position: Position, side: Side) -> bool:
    """Return ``True`` if ``side`` is checkmated."""

    if not is_in_check(position, side):
        return False
    return len(generate_legal_moves(position, side)) == 0


def _apply_move(position: Position, move: Move, next_to_move: Side | None = None) -> Position:
    """Return a new ``Position`` representing ``move`` applied to ``position``."""

    board_copy = Board({coord: piece for coord, piece in position.board})
    board_copy.move_piece(move)
    side_to_move = next_to_move if next_to_move is not None else position.side_to_move.opponent()
    return Position(board=board_copy, side_to_move=side_to_move)
