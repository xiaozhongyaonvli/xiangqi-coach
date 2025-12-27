import pytest

from xiangqi_core import Coord, Move, ParseMoveError


def test_move_from_str_and_to_str_round_trip():
    move = Move.from_str("a0b3")
    assert move.frm == Coord.from_str("a0")
    assert move.to == Coord.from_str("b3")
    assert move.to_str() == "a0b3"


@pytest.mark.parametrize("text", ["", "a0", "a0b", "a0b10", "k0a1", "a-1b0"])
def test_move_from_str_invalid_inputs(text):
    with pytest.raises(ParseMoveError):
        Move.from_str(text)


def test_move_from_str_rejects_non_string():
    with pytest.raises(ParseMoveError):
        Move.from_str(123)  # type: ignore[arg-type]
