from typing import Sequence

from abc import abstractmethod

from square import Square
from constants import PieceColor
from base import BaseDrawable


class BasePiece(BaseDrawable):
	"""The base piece class. Represents a piece on the chessboard."""
	points: int = None  # how much the piece is worth
	notation: str = None  # how the piece is represented in chess notation

	def __init__(self, color: PieceColor, square: Square):
		"""Initialize a piece with a color and square."""
		self.color = color
		self.square = square
	
	@abstractmethod
	def get_movable_squares(self, squares: Sequence[Square]) -> Sequence[Square]:
		"""Get the valid squares the piece can move to."""
		raise NotImplemented

	def __str__(self):
		colorname = 'Light' if self.color == PieceColor.LIGHT else 'Dark'
		return f'{colorname} {self.__class__.__name__} on {self.square.coordinates}'

	def __repr__(self):
		return str(self)


class Pawn(BasePiece):
	"""Represents a pawn on the chessboard."""
	points = 1

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.has_moved = False

	def get_movable_squares(self, squares):
		pass

	def render(self, surface):
		pass


class Bishop(BasePiece):
	"""Represents a bishop on the chessboard."""
	points = 3
	notation = 'B'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_movable_squares(self, squares):
		pass

	def render(self, surface):
		pass


class Knight(BasePiece):
	"""Represents a knight on the chessboard."""
	points = 3
	notation = 'N'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_movable_squares(self, squares):
		pass

	def render(self, surface):
		pass


class Rook(BasePiece):
	"""Represents a rook on the chessboard."""
	points = 5
	notation = 'R'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_movable_squares(self, squares):
		pass

	def render(self, surface):
		pass


class Queen(BasePiece):
	"""Represents a queen on the chessboard."""
	points = 9
	notation = 'Q'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_movable_squares(self, squares):
		pass

	def render(self, surface):
		pass


class King(BasePiece):
	"""Represents a king on the chessboard."""
	notation = 'K'

	def __init__(self, *args, **kwargs):
		self._has_moved = False
		super().__init__(*args, **kwargs)

	def get_movable_squares(self, squares):
		pass

	def render(self, surface):
		pass
