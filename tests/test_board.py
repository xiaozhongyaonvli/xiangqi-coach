import pytest

from xiangqi_core import (
    Board,
    Coord,
    IllegalMoveError,
    Move,
    Piece,
    PieceType,
    Side,
    initial_position,
)


def test_initial_position_piece_layout():
    position = initial_position()
    board = position.board

    assert position.side_to_move is Side.RED
    assert len(list(board.items())) == 32

    # Red back rank
    assert board.get(Coord.from_str("a0")).type is PieceType.ROOK
    assert board.get(Coord.from_str("e0")).type is PieceType.KING
    assert board.get(Coord.from_str("h0")).type is PieceType.HORSE

    # Black back rank
    assert board.get(Coord.from_str("e9")).side is Side.BLACK
    assert board.get(Coord.from_str("i9")).type is PieceType.ROOK

    # Cannons and pawns
    assert board.get(Coord.from_str("b2")).type is PieceType.CANNON
    assert board.get(Coord.from_str("h7")).side is Side.BLACK
    assert board.get(Coord.from_str("c3")).type is PieceType.PAWN
    assert board.get(Coord.from_str("i6")).side is Side.BLACK


def test_move_piece_and_capture():
    board = Board({Coord(0, 0): Piece(Side.RED, PieceType.ROOK)})
    move = Move(Coord(0, 0), Coord(0, 5))
    captured = board.move_piece(move)
    assert captured is None
    assert board.get(Coord(0, 5)).type is PieceType.ROOK
    assert board.get(Coord(0, 0)) is None

    # Add an opposing piece to capture
    board.place(Coord(1, 5), Piece(Side.BLACK, PieceType.PAWN))
    capture_move = Move(Coord(0, 5), Coord(1, 5))
    captured_piece = board.move_piece(capture_move)
    assert captured_piece is not None
    assert captured_piece.side is Side.BLACK
    assert board.get(Coord(1, 5)).type is PieceType.ROOK


def test_move_from_empty_square_raises():
    board = Board()
    with pytest.raises(IllegalMoveError):
        board.move_piece(Move(Coord(0, 0), Coord(0, 1)))
