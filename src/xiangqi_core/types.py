"""Common enumerations used across the Xiangqi rules engine.

The enums defined here are intentionally small and opinionated to keep
the rest of the codebase type-safe and readable.
"""

from __future__ import annotations

from enum import Enum


class Side(str, Enum):
    """Represents the side of a piece or player.

    The values are lowercase strings to make serialization straightforward.
    """

    RED = "red"
    BLACK = "black"

    def opponent(self) -> "Side":
        """Return the opposing side.

        Examples
        --------
        >>> Side.RED.opponent()
        <Side.BLACK: 'black'>
        >>> Side.BLACK.opponent()
        <Side.RED: 'red'>
        """

        return Side.BLACK if self is Side.RED else Side.RED

    @classmethod
    def from_str(cls, value: str) -> "Side":
        """Parse a ``Side`` value from a string.

        Parameters
        ----------
        value:
            Any case-insensitive representation of ``"red"`` or ``"black"``.

        Raises
        ------
        ValueError
            If ``value`` does not correspond to a known side.
        """

        normalized = value.strip().lower()
        try:
            return cls(normalized)
        except ValueError as exc:  # pragma: no cover - defensive branch
            raise ValueError(f"Invalid side: {value}") from exc


class PieceType(str, Enum):
    """Enumerates the seven distinct Xiangqi piece types."""

    KING = "king"
    ADVISOR = "advisor"
    ELEPHANT = "elephant"
    HORSE = "horse"
    ROOK = "rook"
    CANNON = "cannon"
    PAWN = "pawn"
