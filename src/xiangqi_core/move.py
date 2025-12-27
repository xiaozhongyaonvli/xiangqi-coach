"""Move representation for Xiangqi."""

from __future__ import annotations

from dataclasses import dataclass

from xiangqi_core.coord import Coord
from xiangqi_core.errors import ParseCoordError, ParseMoveError


@dataclass(frozen=True, slots=True)
class Move:
    """Represents a move from one coordinate to another."""

    frm: Coord
    to: Coord

    def __post_init__(self) -> None:
        if not isinstance(self.frm, Coord) or not isinstance(self.to, Coord):
            raise TypeError("Move endpoints must be Coord instances")

    def to_str(self) -> str:
        """Return a compact string representation like ``\"a0b3\"``."""

        return f"{self.frm.to_str()}{self.to.to_str()}"

    @classmethod
    def from_str(cls, value: str) -> "Move":
        """Parse a ``Move`` from a string containing two coordinates."""

        if not isinstance(value, str):
            raise ParseMoveError("Move must be a string")

        normalized = value.strip().lower()
        if len(normalized) != 4:
            raise ParseMoveError(f"Invalid move format: {value}")

        try:
            frm = Coord.from_str(normalized[:2])
            to = Coord.from_str(normalized[2:])
        except ParseCoordError as exc:
            raise ParseMoveError(f"Invalid move coordinates: {value}") from exc

        return cls(frm=frm, to=to)
