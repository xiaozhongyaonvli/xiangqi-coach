"""Game state machine coordinating move application and results."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from xiangqi_core.board import Position, initial_position
from xiangqi_core.errors import GameOverError, IllegalMoveError
from xiangqi_core.legality import generate_legal_moves, is_checkmate, is_legal_move
from xiangqi_core.move import Move
from xiangqi_core.types import PieceType, Side


class GameResult(str, Enum):
    """Represents the end state of a game."""

    ONGOING = "ongoing"
    RED_WIN = "red_win"
    BLACK_WIN = "black_win"


class Game:
    """Encapsulates an in-progress Xiangqi game."""

    def __init__(self, position: Optional[Position] = None) -> None:
        self.position: Position = position or initial_position()
        self.history: List[Move] = []
        self.result: GameResult = GameResult.ONGOING

    def apply_move(self, move: Move) -> None:
        """Apply ``move`` if legal, updating game state and result."""

        if self.result is not GameResult.ONGOING:
            raise GameOverError("Game is already finished")

        if not is_legal_move(self, move):
            raise IllegalMoveError(f"Illegal move: {move.to_str()}")

        captured = self.position.board.move_piece(move)
        self.history.append(move)
        self.position.side_to_move = self.position.side_to_move.opponent()

        if captured is not None and captured.type is PieceType.KING:
            self.result = GameResult.RED_WIN if captured.side is Side.BLACK else GameResult.BLACK_WIN
            return

        opponent = self.position.side_to_move
        if is_checkmate(self.position, opponent):
            self.result = GameResult.RED_WIN if opponent is Side.BLACK else GameResult.BLACK_WIN

    def legal_moves(self) -> List[Move]:
        """Convenience wrapper for legal move generation for the side to move."""

        return generate_legal_moves(self.position, self.position.side_to_move)
