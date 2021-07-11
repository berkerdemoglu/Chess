from enum import Enum


class ChessColor(Enum):
	"""The color of a square/piece."""
	DARK = -1
	LIGHT = 1

	@classmethod
	def negate(cls, color: 'ChessColor'):
		return cls(-color.value)
