"""
This module defines constants and enumerations regarding the whole application.
"""
from enum import Enum

from pathlib import Path

# Settings
ROOT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / 'assets'
PIECE_DIR = ASSETS_DIR / 'pieces'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game constants
SCREEN_PROPERTIES = (1280, 720)
WINDOW_TITLE = 'Chess'
FPS = 60
BACKGROUND_COLOR = (192, 192, 192)

# Chess-related constants
SQUARE_FONT_COLOR = (32, 30, 31)


# Piece-related constants/enums
class SquareColor(Enum):
	"""The color of a square/piece."""
	DARK = 0
	LIGHT = 1

	@classmethod
	def negate(cls, piece_color: 'SquareColor'):
		return cls.LIGHT if piece_color == cls.DARK else cls.DARK
