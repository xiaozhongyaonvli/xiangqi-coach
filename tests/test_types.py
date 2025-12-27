import pytest

from xiangqi_core import PieceType, Side


def test_side_opponent_round_trip():
    assert Side.RED.opponent() is Side.BLACK
    assert Side.BLACK.opponent() is Side.RED


@pytest.mark.parametrize(
    "value, expected",
    [
        ("red", Side.RED),
        ("RED", Side.RED),
        (" Red  ", Side.RED),
        ("black", Side.BLACK),
        ("BLACK", Side.BLACK),
        (" Black  ", Side.BLACK),
    ],
)
def test_side_from_str_valid(value, expected):
    assert Side.from_str(value) is expected


def test_side_from_str_invalid():
    with pytest.raises(ValueError):
        Side.from_str("blue")


def test_piece_types_are_string_enums():
    assert PieceType.KING.value == "king"
    assert PieceType.PAWN.value == "pawn"


def test_all_exported():
    assert "Side" in __import__("xiangqi_core").__all__
    assert "PieceType" in __import__("xiangqi_core").__all__
