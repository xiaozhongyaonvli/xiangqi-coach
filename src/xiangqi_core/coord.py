"""Coordinate utilities for the Xiangqi board (9 columns x 10 rows)."""

from __future__ import annotations

from dataclasses import dataclass

from xiangqi_core.errors import ParseCoordError

_FILE_TO_INDEX = {char: idx for idx, char in enumerate("abcdefghi")}
_INDEX_TO_FILE = "abcdefghi"


@dataclass(frozen=True, slots=True)
class Coord:
    """Immutable board coordinate using 0-based indexing."""

    x: int
    y: int

    def __post_init__(self) -> None:
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise TypeError("Coord coordinates must be integers")

    def to_str(self) -> str:
        """Return ICCS-style string representation (e.g., ``\"e2\"``)."""

        if not self.in_bounds():
            raise ValueError(f"Coordinate out of bounds: {self}")
        return f"{_INDEX_TO_FILE[self.x]}{self.y}"

    def in_bounds(self) -> bool:
        """Return ``True`` if the coordinate lies on a 9x10 board."""

        return 0 <= self.x <= 8 and 0 <= self.y <= 9

    @classmethod
    def from_str(cls, value: str) -> "Coord":
        """Parse a coordinate from a string like ``\"a0\"`` or ``\"i9\"``."""

        if not isinstance(value, str):
            raise ParseCoordError("Coordinate must be a string")
        normalized = value.strip().lower()
        if len(normalized) != 2:
            raise ParseCoordError(f"Invalid coordinate format: {value}")
        file_char, rank_char = normalized[0], normalized[1]
        if file_char not in _FILE_TO_INDEX:
            raise ParseCoordError(f"Invalid file in coordinate: {value}")
        if not rank_char.isdigit():
            raise ParseCoordError(f"Invalid rank in coordinate: {value}")
        x = _FILE_TO_INDEX[file_char]
        y = int(rank_char)
        coord = cls(x=x, y=y)
        if not coord.in_bounds():
            raise ParseCoordError(f"Coordinate out of bounds: {value}")
        return coord
