"""Pseudo-legal move validation for Xiangqi pieces."""

from __future__ import annotations

from xiangqi_core.board import Board, Position
from xiangqi_core.coord import Coord
from xiangqi_core.move import Move
from xiangqi_core.types import PieceType, Side


def is_pseudo_legal_move(position: Position, move: Move) -> bool:
    """Return ``True`` if ``move`` satisfies piece geometry and blocking rules.

    This function intentionally ignores turn order and king safety. It only
    validates that the moving piece could travel from ``move.frm`` to
    ``move.to`` according to Xiangqi movement rules and blocking constraints.
    """

    piece = position.board.get(move.frm)
    if piece is None:
        return False
    if move.frm == move.to or not move.to.in_bounds():
        return False

    target_piece = position.board.get(move.to)
    if target_piece is not None and target_piece.side is piece.side:
        return False

    if piece.type is PieceType.ROOK:
        return _is_rook_move(position, move)
    if piece.type is PieceType.CANNON:
        return _is_cannon_move(position, move)
    if piece.type is PieceType.HORSE:
        return _is_horse_move(position, move)
    if piece.type is PieceType.ELEPHANT:
        return _is_elephant_move(position, move, piece.side)
    if piece.type is PieceType.ADVISOR:
        return _is_advisor_move(position, move, piece.side)
    if piece.type is PieceType.KING:
        return _is_king_move(position, move, piece.side)
    if piece.type is PieceType.PAWN:
        return _is_pawn_move(move, piece.side)

    return False


def _is_rook_move(position: Position, move: Move) -> bool:
    if not _is_orthogonal(move):
        return False
    return _count_blockers(position.board, move.frm, move.to) == 0


def _is_cannon_move(position: Position, move: Move) -> bool:
    if not _is_orthogonal(move):
        return False

    blockers = _count_blockers(position.board, move.frm, move.to)
    target_piece = position.board.get(move.to)
    if target_piece is None:
        return blockers == 0
    return blockers == 1


def _is_horse_move(position: Position, move: Move) -> bool:
    dx = move.to.x - move.frm.x
    dy = move.to.y - move.frm.y
    if (abs(dx), abs(dy)) not in {(1, 2), (2, 1)}:
        return False

    if abs(dx) == 2:
        block_square = Coord(move.frm.x + dx // 2, move.frm.y)
    else:
        block_square = Coord(move.frm.x, move.frm.y + dy // 2)

    return position.board.get(block_square) is None


def _is_elephant_move(position: Position, move: Move, side: Side) -> bool:
    dx = move.to.x - move.frm.x
    dy = move.to.y - move.frm.y
    if abs(dx) != 2 or abs(dy) != 2:
        return False

    if side is Side.RED and move.to.y > 4:
        return False
    if side is Side.BLACK and move.to.y < 5:
        return False

    block_square = Coord(move.frm.x + dx // 2, move.frm.y + dy // 2)
    return position.board.get(block_square) is None


def _is_advisor_move(position: Position, move: Move, side: Side) -> bool:
    dx = abs(move.to.x - move.frm.x)
    dy = abs(move.to.y - move.frm.y)
    if dx != 1 or dy != 1:
        return False
    return _in_palace(move.to, side)


def _is_king_move(position: Position, move: Move, side: Side) -> bool:
    dx = abs(move.to.x - move.frm.x)
    dy = abs(move.to.y - move.frm.y)
    if dx + dy != 1:
        return False
    return _in_palace(move.to, side)


def _is_pawn_move(move: Move, side: Side) -> bool:
    dx = move.to.x - move.frm.x
    dy = move.to.y - move.frm.y
    forward = 1 if side is Side.RED else -1
    crossed_river = move.frm.y >= 5 if side is Side.RED else move.frm.y <= 4

    if dx == 0 and dy == forward:
        return True
    if crossed_river and abs(dx) == 1 and dy == 0:
        return True
    return False


def _count_blockers(board: Board, start: Coord, end: Coord) -> int:
    """Return number of pieces strictly between ``start`` and ``end``."""

    dx = end.x - start.x
    dy = end.y - start.y
    step_x = (dx > 0) - (dx < 0)
    step_y = (dy > 0) - (dy < 0)

    x, y = start.x + step_x, start.y + step_y
    blockers = 0
    while (x, y) != (end.x, end.y):
        if board.get(Coord(x, y)) is not None:
            blockers += 1
        x += step_x
        y += step_y
    return blockers


def _is_orthogonal(move: Move) -> bool:
    return move.frm.x == move.to.x or move.frm.y == move.to.y


def _in_palace(coord: Coord, side: Side) -> bool:
    if side is Side.RED:
        return 3 <= coord.x <= 5 and 0 <= coord.y <= 2
    return 3 <= coord.x <= 5 and 7 <= coord.y <= 9
