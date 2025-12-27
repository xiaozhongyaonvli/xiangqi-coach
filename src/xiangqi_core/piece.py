"""Piece definitions for Xiangqi."""

from __future__ import annotations

from dataclasses import dataclass

from xiangqi_core.types import PieceType, Side


@dataclass(frozen=True, slots=True)
class Piece:
    """Immutable representation of a Xiangqi piece without board position."""

    side: Side
    type: PieceType

    def __str__(self) -> str:
        return f"{self.side.value}:{self.type.value}"
