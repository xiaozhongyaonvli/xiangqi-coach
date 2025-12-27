import pytest

from xiangqi_core import (
    Board,
    Coord,
    Move,
    Piece,
    PieceType,
    Position,
    Side,
    is_pseudo_legal_move,
)


def test_rook_requires_clear_path() -> None:
    board = Board({Coord(0, 0): Piece(Side.RED, PieceType.ROOK)})
    position = Position(board=board, side_to_move=Side.RED)
    assert is_pseudo_legal_move(position, Move(Coord(0, 0), Coord(0, 5)))

    blocked_board = Board(
        {
            Coord(0, 0): Piece(Side.RED, PieceType.ROOK),
            Coord(0, 3): Piece(Side.RED, PieceType.PAWN),
        }
    )
    blocked_pos = Position(board=blocked_board, side_to_move=Side.RED)
    assert not is_pseudo_legal_move(blocked_pos, Move(Coord(0, 0), Coord(0, 5)))


def test_cannon_needs_screen_to_capture() -> None:
    clear_board = Board(
        {
            Coord(0, 0): Piece(Side.RED, PieceType.CANNON),
        }
    )
    clear_pos = Position(board=clear_board, side_to_move=Side.RED)
    assert is_pseudo_legal_move(clear_pos, Move(Coord(0, 0), Coord(0, 5)))

    capture_board = Board(
        {
            Coord(0, 0): Piece(Side.RED, PieceType.CANNON),
            Coord(0, 1): Piece(Side.RED, PieceType.PAWN),
            Coord(0, 3): Piece(Side.BLACK, PieceType.ROOK),
        }
    )
    capture_pos = Position(board=capture_board, side_to_move=Side.RED)
    assert is_pseudo_legal_move(capture_pos, Move(Coord(0, 0), Coord(0, 3)))

    two_screens_board = Board(
        {
            Coord(0, 0): Piece(Side.RED, PieceType.CANNON),
            Coord(0, 1): Piece(Side.RED, PieceType.PAWN),
            Coord(0, 2): Piece(Side.BLACK, PieceType.PAWN),
            Coord(0, 3): Piece(Side.BLACK, PieceType.ROOK),
        }
    )
    two_screens_pos = Position(board=two_screens_board, side_to_move=Side.RED)
    assert not is_pseudo_legal_move(two_screens_pos, Move(Coord(0, 0), Coord(0, 3)))


def test_horse_blocked_by_leg() -> None:
    blocked_board = Board(
        {
            Coord(4, 4): Piece(Side.RED, PieceType.HORSE),
            Coord(4, 5): Piece(Side.BLACK, PieceType.PAWN),
        }
    )
    blocked_pos = Position(board=blocked_board, side_to_move=Side.RED)
    assert not is_pseudo_legal_move(blocked_pos, Move(Coord(4, 4), Coord(5, 6)))

    open_board = Board({Coord(4, 4): Piece(Side.RED, PieceType.HORSE)})
    open_pos = Position(board=open_board, side_to_move=Side.RED)
    assert is_pseudo_legal_move(open_pos, Move(Coord(4, 4), Coord(5, 6)))


def test_elephant_and_advisor_restrictions() -> None:
    elephant_board = Board({Coord(4, 4): Piece(Side.RED, PieceType.ELEPHANT)})
    elephant_pos = Position(board=elephant_board, side_to_move=Side.RED)
    assert not is_pseudo_legal_move(elephant_pos, Move(Coord(4, 4), Coord(2, 6)))

    blocked_elephant_board = Board(
        {
            Coord(4, 4): Piece(Side.RED, PieceType.ELEPHANT),
            Coord(3, 3): Piece(Side.BLACK, PieceType.PAWN),
        }
    )
    blocked_elephant_pos = Position(board=blocked_elephant_board, side_to_move=Side.RED)
    assert not is_pseudo_legal_move(blocked_elephant_pos, Move(Coord(4, 4), Coord(2, 2)))

    advisor_board = Board({Coord(4, 1): Piece(Side.RED, PieceType.ADVISOR)})
    advisor_pos = Position(board=advisor_board, side_to_move=Side.RED)
    assert is_pseudo_legal_move(advisor_pos, Move(Coord(4, 1), Coord(5, 2)))
    assert not is_pseudo_legal_move(advisor_pos, Move(Coord(4, 1), Coord(6, 3)))


def test_king_stays_in_palace() -> None:
    board = Board({Coord(4, 1): Piece(Side.RED, PieceType.KING)})
    position = Position(board=board, side_to_move=Side.RED)

    assert is_pseudo_legal_move(position, Move(Coord(4, 1), Coord(4, 2)))
    assert not is_pseudo_legal_move(position, Move(Coord(4, 1), Coord(4, 3)))
    assert not is_pseudo_legal_move(position, Move(Coord(4, 1), Coord(2, 1)))


@pytest.mark.parametrize(
    ("frm", "to", "expected"),
    [
        (Coord(4, 3), Coord(4, 4), True),
        (Coord(4, 3), Coord(3, 3), False),
        (Coord(4, 3), Coord(4, 2), False),
        (Coord(4, 5), Coord(3, 5), True),
        (Coord(4, 5), Coord(4, 4), False),
    ],
)
def test_red_pawn_progression(frm: Coord, to: Coord, expected: bool) -> None:
    board = Board({frm: Piece(Side.RED, PieceType.PAWN)})
    position = Position(board=board, side_to_move=Side.RED)
    assert is_pseudo_legal_move(position, Move(frm, to)) is expected


@pytest.mark.parametrize(
    ("frm", "to", "expected"),
    [
        (Coord(4, 6), Coord(4, 5), True),
        (Coord(4, 6), Coord(5, 6), False),
        (Coord(4, 6), Coord(4, 7), False),
        (Coord(4, 4), Coord(5, 4), True),
        (Coord(4, 4), Coord(4, 5), False),
    ],
)
def test_black_pawn_progression(frm: Coord, to: Coord, expected: bool) -> None:
    board = Board({frm: Piece(Side.BLACK, PieceType.PAWN)})
    position = Position(board=board, side_to_move=Side.BLACK)
    assert is_pseudo_legal_move(position, Move(frm, to)) is expected
