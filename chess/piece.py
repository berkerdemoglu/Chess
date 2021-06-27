# Type annotations
from typing import Sequence

from abc import abstractmethod

import pygame as pg

from .square import Square
from .chess_constants import ChessColor
from constants import PIECE_DIR
from graphics import Renderable


class BasePiece(Renderable):
	"""The base piece class. Represents a piece on the chessboard."""

	# Dicts
	PIECE_DICT = {
		'Pawn': 'p', 'Knight': 'n', 'Bishop': 'b',
		'Rook': 'r', 'Queen': 'q', 'King': 'k'
	}

	points: int  # how much the piece is worth
	notation: str  # how the piece is represented in chess notation

	def __init__(self, color: ChessColor, square: Square):
		"""Initialize a piece with a color and square."""
		self.color = color
		self.square = square

		# Load image and get its rect
		imagename = f"{'w' if self.color == ChessColor.LIGHT else 'b'}" \
			f"{self.__class__.notation.lower()}.png"
		self.image = pg.image.load(PIECE_DIR / imagename).convert_alpha()

		self.rect = self.image.get_rect()

	def center_in_square(self, surface: pg.Surface):
		square_pos = self.square.get_pos(surface)
		self.rect.centerx = square_pos[0] + Square.SQUARE_SIZE // 2
		self.rect.centery = square_pos[1] + Square.SQUARE_SIZE // 2

	def set_pos(self, x: float, y: float):
		self.rect.centerx = x
		self.rect.centery = y

	@abstractmethod
	def get_possible_moves(self, squares: Sequence[Square]) -> Sequence[Square]:
		"""Get the valid squares the piece can move to."""
		raise NotImplemented

	def render(self, surface: pg.Surface) -> None:
		"""Renders the piece to the screen."""
		surface.blit(self.image, self.rect)

	def __str__(self):
		colorname = 'Light' if self.color == ChessColor.LIGHT else 'Dark'
		return f'{colorname} {self.__class__.__name__} on {self.square.coordinates}'

	def __repr__(self):
		return str(self)


class Pawn(BasePiece):
	"""Represents a pawn on the chessboard."""
	points = 1
	notation = 'P'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.has_moved = False

	def get_possible_moves(self, squares):
		pass


class Bishop(BasePiece):
	"""Represents a bishop on the chessboard."""
	points = 3
	notation = 'B'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_possible_moves(self, squares):
		pass


class Knight(BasePiece):
	"""Represents a knight on the chessboard."""
	points = 3
	notation = 'N'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_possible_moves(self, squares):
		pass


class Rook(BasePiece):
	"""Represents a rook on the chessboard."""
	points = 5
	notation = 'R'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_possible_moves(self, squares):
		pass


class Queen(BasePiece):
	"""Represents a queen on the chessboard."""
	points = 9
	notation = 'Q'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_possible_moves(self, squares):
		pass


class King(BasePiece):
	"""Represents a king on the chessboard."""
	notation = 'K'

	def __init__(self, *args, **kwargs):
		self._has_moved = False
		super().__init__(*args, **kwargs)

	def get_possible_moves(self, squares):
		pass
