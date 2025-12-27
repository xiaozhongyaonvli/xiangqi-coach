"""Board and position structures for Xiangqi."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, Mapping, Optional, Tuple

from xiangqi_core.coord import Coord
from xiangqi_core.errors import IllegalMoveError
from xiangqi_core.move import Move
from xiangqi_core.piece import Piece
from xiangqi_core.types import PieceType, Side


class Board:
    """Sparse board representation backed by a dictionary."""

    def __init__(self, pieces: Optional[Mapping[Coord, Piece]] = None) -> None:
        self._grid: Dict[Coord, Piece] = {}
        if pieces:
            for coord, piece in pieces.items():
                self._validate_coord(coord)
                self._grid[coord] = piece

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._grid)

    def __iter__(self) -> Iterator[Tuple[Coord, Piece]]:  # pragma: no cover
        return iter(self._grid.items())

    @staticmethod
    def _validate_coord(coord: Coord) -> None:
        if not isinstance(coord, Coord):
            raise TypeError("Board keys must be Coord instances")
        if not coord.in_bounds():
            raise ValueError(f"Coordinate out of bounds: {coord}")

    def get(self, coord: Coord) -> Optional[Piece]:
        """Return the piece at ``coord`` or ``None`` if empty."""

        self._validate_coord(coord)
        return self._grid.get(coord)

    def place(self, coord: Coord, piece: Piece) -> None:
        """Place ``piece`` on ``coord`` (overwriting any existing piece)."""

        self._validate_coord(coord)
        self._grid[coord] = piece

    def remove(self, coord: Coord) -> Optional[Piece]:
        """Remove and return the piece at ``coord`` if present."""

        self._validate_coord(coord)
        return self._grid.pop(coord, None)

    def move_piece(self, move: Move) -> Optional[Piece]:
        """Execute ``move`` on the board and return any captured piece."""

        self._validate_coord(move.frm)
        self._validate_coord(move.to)
        piece = self._grid.get(move.frm)
        if piece is None:
            raise IllegalMoveError(f"No piece at source square {move.frm}")
        captured = self._grid.get(move.to)
        self._grid.pop(move.frm)
        self._grid[move.to] = piece
        return captured

    def items(self) -> Iterable[Tuple[Coord, Piece]]:  # pragma: no cover
        return self._grid.items()


@dataclass
class Position:
    board: Board
    side_to_move: Side


def initial_position() -> Position:
    """Return the standard Xiangqi starting position."""

    board = Board()

    def _place_back_rank(side: Side, y: int) -> None:
        pieces = [
            PieceType.ROOK,
            PieceType.HORSE,
            PieceType.ELEPHANT,
            PieceType.ADVISOR,
            PieceType.KING,
            PieceType.ADVISOR,
            PieceType.ELEPHANT,
            PieceType.HORSE,
            PieceType.ROOK,
        ]
        for x, piece_type in enumerate(pieces):
            board.place(Coord(x, y), Piece(side=side, type=piece_type))

    def _place_cannons(side: Side, y: int) -> None:
        for x in (1, 7):
            board.place(Coord(x, y), Piece(side=side, type=PieceType.CANNON))

    def _place_pawns(side: Side, y: int) -> None:
        for x in (0, 2, 4, 6, 8):
            board.place(Coord(x, y), Piece(side=side, type=PieceType.PAWN))

    _place_back_rank(Side.RED, 0)
    _place_cannons(Side.RED, 2)
    _place_pawns(Side.RED, 3)

    _place_back_rank(Side.BLACK, 9)
    _place_cannons(Side.BLACK, 7)
    _place_pawns(Side.BLACK, 6)

    return Position(board=board, side_to_move=Side.RED)
