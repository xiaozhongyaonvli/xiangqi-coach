from xiangqi_core import (
    Board,
    Coord,
    Game,
    GameResult,
    Move,
    Piece,
    PieceType,
    Position,
    Side,
    generate_legal_moves,
    is_checkmate,
    is_legal_move,
)


def test_move_exposing_king_is_illegal() -> None:
    board = Board(
        {
            Coord(4, 1): Piece(Side.RED, PieceType.KING),
            Coord(4, 3): Piece(Side.RED, PieceType.ROOK),
            Coord(4, 9): Piece(Side.BLACK, PieceType.ROOK),
            Coord(3, 9): Piece(Side.BLACK, PieceType.KING),
        }
    )
    position = Position(board=board, side_to_move=Side.RED)
    game = Game(position=position)

    unsafe_move = Move(Coord(4, 3), Coord(3, 3))
    assert not is_legal_move(game, unsafe_move)

    safe_move = Move(Coord(4, 3), Coord(4, 9))
    assert is_legal_move(game, safe_move)


def test_checkmate_detection_and_legal_move_generation() -> None:
    board = Board(
        {
            Coord(4, 1): Piece(Side.RED, PieceType.KING),
            Coord(4, 7): Piece(Side.RED, PieceType.ROOK),
            Coord(3, 8): Piece(Side.RED, PieceType.ROOK),
            Coord(6, 7): Piece(Side.RED, PieceType.HORSE),
            Coord(6, 8): Piece(Side.RED, PieceType.PAWN),
            Coord(4, 9): Piece(Side.BLACK, PieceType.KING),
        }
    )
    position = Position(board=board, side_to_move=Side.RED)
    game = Game(position=position)

    finishing_move = Move(Coord(6, 8), Coord(5, 8))
    game.apply_move(finishing_move)

    assert game.result is GameResult.RED_WIN
    assert position.side_to_move is Side.BLACK
    assert is_checkmate(position, Side.BLACK)
    assert generate_legal_moves(position, Side.BLACK) == []
