# Type annotations
from typing import List, Sequence, Callable, TYPE_CHECKING
if TYPE_CHECKING:
	from .board import Board

# Utility imports
from abc import abstractmethod
from functools import wraps

import pygame as pg

from settings import PIECE_DIR
from graphics import Renderable

# Chess imports
from .square import Square
from .chess_constants import ChessColor, Direction


__all__ = [
	'BasePiece', 'Pawn', 'Bishop',
	'Knight', 'Rook', 'Queen', 'King'
]


#############################
######### UTILITIES #########
#############################


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


class RenderablePiece(Renderable):

	def __init__(self, color: ChessColor, square: Square):
		"""Initialize a piece with a color, square, and image and rect."""
		self.color = color
		self.square = square

		# Load image and get its rect
		# P.S: the notation attribute is implemented later on, ignore this error
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


class BasePiece(RenderablePiece):
	"""The base piece class. Represents a piece on the chessboard."""

	# Constants
	PIECE_DICT = {
		'Pawn': 'p', 'Knight': 'n', 'Bishop': 'b',
		'Rook': 'r', 'Queen': 'q', 'King': 'k'
	}

	HORIZONTAL_DIRECTIONS = (Direction.LEFT, Direction.RIGHT)
	VERTICAL_DIRECTIONS = (Direction.FORWARD, Direction.BACK)

	# Class attributes
	points: int  # how much the piece is worth
	notation: str  # how the piece is represented in chess notation

	def __init__(self, color: ChessColor, square: Square, surface: pg.Surface):
		super().__init__(color, square)

		self.center_in_square(surface)

	# Chess-related methods
	@abstractmethod
	def get_possible_moves(self, board: 'Board') -> List[Square]:
		"""Get the valid squares the piece can move to."""
		raise NotImplemented

	def add_move(
		self, board_squares: List[Square], possible_squares: List[Square], 
		*directions: Direction
		):
		"""
		Add a square to the possible squares list by adding up the directions. 
		Keep in mind that this does not account for pieces on the way to said
		square (like a knight). 
		"""
		kls = type(self)

		horizontal_increment = 0
		vertical_increment = 0

		for direction in directions:
			if direction in kls.HORIZONTAL_DIRECTIONS:
				horizontal_increment += direction.value * self.color.value
			elif direction in kls.VERTICAL_DIRECTIONS:
				vertical_increment += direction.value * self.color.value

		horizontal_validity = self._check_can_move_horizontal(horizontal_increment)
		vertical_validity = self._check_can_move_vertical(vertical_increment)

		is_valid_move = horizontal_validity and vertical_validity

		if is_valid_move:
			total_increment = horizontal_increment + vertical_increment
			new_square_index = self.square.index + total_increment

			possible_squares.append(board_squares[new_square_index])

	def _check_can_move_horizontal(self, direction_increment: int) -> bool:
		"""Check if the piece can move in a certain horizontal direction."""
		i = self.square.index

		row_current = i // 8
		row_after = (i + direction_increment) // 8

		if row_current != row_after:
			# Piece cannot move in this direction any further
			return False

		return True

	def _check_can_move_vertical(self, direction_increment: int) -> bool:
		"""Check if the piece can move in a certain vertical direction."""
		new_square_index = self.square.index + direction_increment

		if new_square_index < 0 or new_square_index >= 64:
			return False

		return True


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
	def get_possible_moves(self, board):
		# TODO: Promotions
		# TODO: En-passant

		squares = board.squares
		possible_squares = list()
		i = self.square.index

		# Get the forward direction increment
		forward: int = Direction.FORWARD.value * self.color.value

		# First of all, check if the pawn can move forward.
		if self._check_can_move_vertical(forward):
			# One square forward
			move_square = squares[i + forward]
			piece_in_front_of_me = board.get_piece_occupying_square(move_square)

			if piece_in_front_of_me is None:
				if self._check_can_move_vertical(forward):
					possible_squares.append(move_square)

			# Two squares forward
			if not self.has_moved and piece_in_front_of_me is None:
				possible_squares.append(squares[i + 2*forward])

			# Get left and right directions to be used for captures
			left: int = Direction.LEFT.value * self.color.value
			right: int = Direction.RIGHT.value * self.color.value

			# Left diagonal capture
			if self._check_can_move_horizontal(left):
				left_diagonal_capture_square = squares[i + forward + left]
				if board.get_piece_occupying_square(left_diagonal_capture_square) is not None:
					possible_squares.append(left_diagonal_capture_square)

			# Right diagonal capture
			if self._check_can_move_horizontal(right):
				right_diagonal_capture_square = squares[i + forward + right]
				if board.get_piece_occupying_square(right_diagonal_capture_square) is not None:
					possible_squares.append(right_diagonal_capture_square)

		return possible_squares


class Bishop(BasePiece):
	"""Represents a bishop on the chessboard."""
	points = 3
	notation = 'B'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, board):
		return []


class Knight(BasePiece):
	"""Represents a knight on the chessboard."""
	points = 3
	notation = 'N'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, board):
		return []


class Rook(BasePiece):
	"""Represents a rook on the chessboard."""
	points = 5
	notation = 'R'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, board):
		return []


class Queen(BasePiece):
	"""Represents a queen on the chessboard."""
	points = 9
	notation = 'Q'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, board):
		return []


class King(BasePiece):
	"""Represents a king on the chessboard."""
	notation = 'K'

	def __init__(self, *args, **kwargs):
		self.has_moved = False
		super().__init__(*args, **kwargs)

	@highlight_squares
	def get_possible_moves(self, board):
		return []
