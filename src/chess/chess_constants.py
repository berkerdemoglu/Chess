from enum import Enum


class ChessColor(Enum):
	"""The color of a square/piece."""
	DARK = -1
	LIGHT = 1

	@classmethod
	def negate(cls, chess_color: 'ChessColor'):
		return cls.LIGHT if chess_color == cls.DARK else cls.DARK
