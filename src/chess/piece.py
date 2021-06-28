# Type annotations
from typing import List, Callable, Tuple

from abc import abstractmethod
from functools import wraps

import pygame as pg

from .square import Square
from .chess_constants import ChessColor
from settings import PIECE_DIR
from graphics import Renderable


############################
######## DECORATORS ########
############################


def highlight_squares(func: Callable):
	"""Return a method that returns a list of squares and highlights those squares."""
	@wraps(func)
	def wrapper(self, *args, **kwargs):
		possible_squares = func(self, *args, **kwargs)
		for square in possible_squares:
			square.highlight(Square.VALID_MOVE_HIGHLIGHT)

		return possible_squares

	return wrapper


################################
######### BASE CLASSES #########
################################


class PieceRenderable(Renderable):

	def __init__(self, color: ChessColor, square: Square):
		"""Initialize a piece with a color, square, and image and rect."""
		self.color = color
		self.square = square

		# Load image and get its rect
		imagename = f"{'w' if self.color == ChessColor.LIGHT else 'b'}" \
			f"{self.__class__.notation.lower()}.png"
		self.image = pg.image.load(PIECE_DIR / imagename).convert_alpha()

		self.rect = self.image.get_rect()

	# Graphics methods
	def render(self, surface: pg.Surface) -> None:
		"""Renders the piece to the screen."""
		surface.blit(self.image, self.rect)

	def center_in_square(self, surface: pg.Surface):
		"""Center the piece's rect."""
		square_pos = self.square.get_pos(surface)
		self.rect.centerx = square_pos[0] + Square.SQUARE_SIZE // 2
		self.rect.centery = square_pos[1] + Square.SQUARE_SIZE // 2

	def set_pos(self, x: float, y: float):
		"""Set the position of the piece on the screen."""
		self.rect.centerx = x
		self.rect.centery = y

	# String methods
	def __str__(self):
		"""String representation of a piece."""
		colorname = 'Light' if self.color == ChessColor.LIGHT else 'Dark'
		return f'{colorname} {self.__class__.__name__} on {self.square.coordinates}'

	def __repr__(self):
		return str(self)


class BasePiece(PieceRenderable):
	"""The base piece class. Represents a piece on the chessboard."""

	# Dicts
	PIECE_DICT = {
		'Pawn': 'p', 'Knight': 'n', 'Bishop': 'b',
		'Rook': 'r', 'Queen': 'q', 'King': 'k'
	}

	# Directions for white. For black, just multiply them by -1.
	DIRECTIONS = {
		'forward': -8,
		'back': 8,
		'right': 1,
		'left': -1
	}

	points: int  # how much the piece is worth
	notation: str  # how the piece is represented in chess notation

	def __init__(self, color: ChessColor, square: Square, surface: pg.Surface):
		super().__init__(color, square)

		self.center_in_square(surface)

	# Chess-related methods
	@abstractmethod
	def get_possible_moves(self, squares: List[Square]) -> List[Square]:
		"""Get the valid squares the piece can move to."""
		raise NotImplemented

	def get_directions(self) -> Tuple[int, int, int, int]:
		return self.get_forward(), self.get_back(), self.get_left(), self.get_right()

	def get_forward(self) -> int:
		return BasePiece.DIRECTIONS['forward'] * self.color.value

	def get_back(self) -> int:
		return BasePiece.DIRECTIONS['back'] * self.color.value

	def get_left(self) -> int:
		return BasePiece.DIRECTIONS['left'] * self.color.value

	def get_right(self) -> int:
		return BasePiece.DIRECTIONS['right'] * self.color.value


################################
######### CHESS PIECES #########
################################


class Pawn(BasePiece):
	"""Represents a pawn on the chessboard."""
	points = 1
	notation = 'P'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.has_moved = False

	@highlight_squares
	def get_possible_moves(self, squares):
		possible_squares = list()
		forward = self.get_forward()
		possible_squares.append(squares[self.square.index + forward])

		return possible_squares


class Bishop(BasePiece):
	"""Represents a bishop on the chessboard."""
	points = 3
	notation = 'B'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, squares):
		pass


class Knight(BasePiece):
	"""Represents a knight on the chessboard."""
	points = 3
	notation = 'N'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, squares):
		pass


class Rook(BasePiece):
	"""Represents a rook on the chessboard."""
	points = 5
	notation = 'R'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, squares):
		pass


class Queen(BasePiece):
	"""Represents a queen on the chessboard."""
	points = 9
	notation = 'Q'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, squares):
		pass


class King(BasePiece):
	"""Represents a king on the chessboard."""
	notation = 'K'

	def __init__(self, *args, **kwargs):
		self._has_moved = False
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, squares):
		pass
