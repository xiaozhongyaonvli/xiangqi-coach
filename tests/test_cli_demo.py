import textwrap

from xiangqi_cli_demo import describe_status, render_board
from xiangqi_core import Game, GameResult, Position
from xiangqi_core.board import Board
from xiangqi_core.coord import Coord
from xiangqi_core.piece import Piece
from xiangqi_core.types import PieceType, Side


def test_render_board_initial_position():
    game = Game()

    expected = textwrap.dedent(
        """\
           a b c d e f g h i
        9  r h e a k a e h r
        8  . . . . . . . . .
        7  . c . . . . . c .
        6  p . p . p . p . p
        5  . . . . . . . . .
        4  . . . . . . . . .
        3  P . P . P . P . P
        2  . C . . . . . C .
        1  . . . . . . . . .
        0  R H E A K A E H R
           a b c d e f g h i"""
    )

    assert render_board(game.position) == expected


def test_describe_status_includes_check_and_results():
    board = Board()
    board.place(Coord(4, 9), Piece(Side.BLACK, PieceType.KING))
    board.place(Coord(0, 0), Piece(Side.RED, PieceType.KING))
    board.place(Coord(4, 0), Piece(Side.RED, PieceType.ROOK))
    position = Position(board=board, side_to_move=Side.BLACK)
    game = Game(position=position)

    assert describe_status(game) == "Side to move: Black | Black is in check"

    game.result = GameResult.RED_WIN
    assert describe_status(game) == "Side to move: Black | Game over — Red wins"
