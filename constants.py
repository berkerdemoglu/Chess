"""
This module defines constants and enumerations regarding the whole application.
"""

from enum import Enum

from pathlib import Path

# Settings
ROOT_DIR = Path(__file__).resolve().parent
PIECE_DIR = (ROOT_DIR / 'assets') / 'pieces'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game constants
SCREEN_PROPERTIES = (1280, 720)
WINDOW_TITLE = 'Chess'
BACKGROUND_COLOR = (192, 192, 192)

SQUARE_FONT_COLOR = (32, 30, 31)


# Piece-related stuff
class PieceColor(Enum):
	"""The color of a piece."""
	LIGHT = 1
	DARK = 0
