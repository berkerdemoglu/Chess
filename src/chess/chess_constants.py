from enum import Enum


class ChessColor(Enum):
	"""The color of a square/piece."""
	DARK = -1
	LIGHT = 1

	@classmethod
	def negate(cls, color: 'ChessColor'):
		return cls(-color.value)


class Direction(Enum):
	"""
	A direction on the board from white's perspective represented by 
	square index differences. For black, just multiply them by -1.
	"""
	FORWARD = -8
	BACK = 8
	RIGHT = 1
	LEFT = -1
