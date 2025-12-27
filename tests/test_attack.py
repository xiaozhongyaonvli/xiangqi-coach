from xiangqi_core import (
    Board,
    Coord,
    Piece,
    PieceType,
    Position,
    Side,
    find_king,
    is_in_check,
    is_square_attacked,
)


def test_rook_and_cannon_attack_detection() -> None:
    rook_board = Board(
        {
            Coord(0, 0): Piece(Side.RED, PieceType.ROOK),
            Coord(0, 3): Piece(Side.BLACK, PieceType.KING),
            Coord(4, 9): Piece(Side.BLACK, PieceType.ROOK),
            Coord(4, 1): Piece(Side.RED, PieceType.KING),
        }
    )
    rook_pos = Position(board=rook_board, side_to_move=Side.RED)
    assert is_square_attacked(rook_pos, Side.RED, Coord(0, 3))
    assert is_in_check(rook_pos, Side.BLACK)

    cannon_board = Board(
        {
            Coord(0, 0): Piece(Side.RED, PieceType.CANNON),
            Coord(0, 1): Piece(Side.BLACK, PieceType.PAWN),
            Coord(0, 3): Piece(Side.BLACK, PieceType.KING),
            Coord(4, 9): Piece(Side.BLACK, PieceType.ROOK),
            Coord(4, 1): Piece(Side.RED, PieceType.KING),
        }
    )
    cannon_pos = Position(board=cannon_board, side_to_move=Side.RED)
    assert is_square_attacked(cannon_pos, Side.RED, Coord(0, 3))

    no_screen_board = Board(
        {
            Coord(0, 0): Piece(Side.RED, PieceType.CANNON),
            Coord(0, 3): Piece(Side.BLACK, PieceType.KING),
            Coord(4, 9): Piece(Side.BLACK, PieceType.ROOK),
            Coord(4, 1): Piece(Side.RED, PieceType.KING),
        }
    )
    no_screen_pos = Position(board=no_screen_board, side_to_move=Side.RED)
    assert not is_square_attacked(no_screen_pos, Side.RED, Coord(0, 3))


def test_face_to_face_kings_count_as_attack() -> None:
    board = Board(
        {
            Coord(4, 1): Piece(Side.RED, PieceType.KING),
            Coord(4, 9): Piece(Side.BLACK, PieceType.KING),
        }
    )
    position = Position(board=board, side_to_move=Side.RED)

    assert is_in_check(position, Side.RED)
    assert is_in_check(position, Side.BLACK)
    assert find_king(position, Side.RED) == Coord(4, 1)
