"""Domain-specific exception types used across the Xiangqi core package."""


class XiangqiError(Exception):
    """Base class for Xiangqi-specific errors."""


class ParseCoordError(ValueError, XiangqiError):
    """Raised when a coordinate string cannot be parsed."""


class ParseMoveError(ValueError, XiangqiError):
    """Raised when a move string cannot be parsed."""


class IllegalMoveError(ValueError, XiangqiError):
    """Raised when a move violates Xiangqi rules."""


class GameOverError(RuntimeError, XiangqiError):
    """Raised when attempting to play a move after the game is finished."""
