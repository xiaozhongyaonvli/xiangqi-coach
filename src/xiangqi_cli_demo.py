"""Minimal CLI demonstration for the Xiangqi core rules.

The CLI is intentionally lightweight and keeps all state in-memory. It should
remain separate from the core rules so the engine can stay UI-agnostic.
"""

from __future__ import annotations

from typing import Iterable, List

from xiangqi_core import (
    Game,
    GameResult,
    Move,
    Position,
    Side,
    XiangqiError,
    is_in_check,
)
from xiangqi_core.board import Board
from xiangqi_core.coord import Coord
from xiangqi_core.piece import Piece
from xiangqi_core.types import PieceType

_PIECE_SYMBOLS = {
    PieceType.KING: "k",
    PieceType.ADVISOR: "a",
    PieceType.ELEPHANT: "e",
    PieceType.HORSE: "h",
    PieceType.ROOK: "r",
    PieceType.CANNON: "c",
    PieceType.PAWN: "p",
}


def _piece_symbol(piece: Piece) -> str:
    """Return a single-character symbol for ``piece``."""

    symbol = _PIECE_SYMBOLS[piece.type]
    return symbol.upper() if piece.side is Side.RED else symbol.lower()


def render_board(position: Position) -> str:
    """Render ``position`` as an ASCII board."""

    header = "   a b c d e f g h i"
    rows: List[str] = [header]
    for y in range(9, -1, -1):
        symbols: Iterable[str] = (
            _piece_symbol(piece) if (piece := position.board.get(Coord(x, y))) else "."
            for x in range(9)
        )
        rows.append(f"{y}  {' '.join(symbols)}")
    rows.append(header)
    return "\n".join(rows)


def describe_status(game: Game) -> str:
    """Summarize the side to move, check status, and result."""

    side_label = "Red" if game.position.side_to_move is Side.RED else "Black"
    parts = [f"Side to move: {side_label}"]

    if game.result is not GameResult.ONGOING:
        winner = "Red" if game.result is GameResult.RED_WIN else "Black"
        parts.append(f"Game over — {winner} wins")
        return " | ".join(parts)

    if is_in_check(game.position, game.position.side_to_move):
        parts.append(f"{side_label} is in check")

    return " | ".join(parts)


def _print_help() -> None:
    print("Enter moves as four characters, e.g., e2e3")
    print("Commands: 'exit' or 'quit' to leave, 'help' to show this message.")


def _prompt() -> str:
    return input("move> ").strip()


def main() -> None:  # pragma: no cover - interactive wrapper
    """Run the interactive CLI demo."""

    game = Game()
    print("Xiangqi CLI demo (from-to format, e.g., a0a1). Type 'help' for info.")
    while True:
        print(render_board(game.position))
        print(describe_status(game))
        if game.result is not GameResult.ONGOING:
            break

        command = _prompt()
        lower = command.lower()
        if lower in {"quit", "exit"}:
            break
        if lower == "help":
            _print_help()
            continue
        if not command:
            continue

        try:
            move = Move.from_str(command)
            game.apply_move(move)
        except XiangqiError as exc:
            print(f"❌ {exc}")


if __name__ == "__main__":  # pragma: no cover - script entrypoint
    main()
