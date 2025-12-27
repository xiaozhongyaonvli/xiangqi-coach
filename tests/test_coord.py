import pytest

from xiangqi_core import Coord, ParseCoordError


def test_coord_to_and_from_str_round_trip():
    coord = Coord.from_str("e2")
    assert coord.to_str() == "e2"
    assert coord.in_bounds()


@pytest.mark.parametrize("text", ["a0", "i9", "C5", " h7 "])
def test_coord_from_str_valid_inputs(text):
    coord = Coord.from_str(text)
    assert coord.in_bounds()
    assert coord.to_str() == coord.to_str().lower()


@pytest.mark.parametrize("text", ["", "j0", "a10", "aa0", "b", "9c", "a-1"])
def test_coord_from_str_invalid_inputs(text):
    with pytest.raises(ParseCoordError):
        Coord.from_str(text)


def test_coord_out_of_bounds_to_str_raises():
    with pytest.raises(ValueError):
        Coord(9, 0).to_str()
