"""Move representation for Xiangqi."""

from __future__ import annotations

from dataclasses import dataclass

from xiangqi_core.coord import Coord


@dataclass(frozen=True, slots=True)
class Move:
    """Represents a move from one coordinate to another."""

    frm: Coord
    to: Coord

    def __post_init__(self) -> None:
        if not isinstance(self.frm, Coord) or not isinstance(self.to, Coord):
            raise TypeError("Move endpoints must be Coord instances")
