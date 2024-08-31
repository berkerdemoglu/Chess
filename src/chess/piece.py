# Type annotations
from typing import List, Sequence, Callable, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
	from .board import Board

# Built-in utilities
from abc import abstractmethod
from functools import wraps

# Pygame
import pygame as pg

# Graphics and settings imports
from graphics import Renderable, Spritesheet, PIECE_SIZE_X, PIECE_SIZE_Y
from settings import ASSETS_DIR

# Chess imports
from .square import Square
from .chess_constants import ChessColor, Direction


# Define what can be imported from this module.
__all__ = [
	'BasePiece', 'FirstMovePiece', 
	'Pawn', 'Bishop', 'Knight', 
	'Rook', 'Queen', 'King', 'PieceCreator'
]


#############################
######### UTILITIES #########
#############################


class PieceCreator:
	"""Creates piece for the game. Handles graphics for them as well."""
	spritesheet = Spritesheet(ASSETS_DIR / 'pieces.png')

	@classmethod
	def create_piece(
			cls, piece_class, color: ChessColor, 
			square: Square, screen: pg.Surface
		):
		"""TODO: Add typing for piece_class and docstring"""
		# Init the piece with chess logic
		piece = piece_class(color, square)

		# Get the rect that covers the area for the sprite.
		y_offset = 0
		if color == ChessColor.DARK:
			y_offset = 64

		image_position_rect = pg.Rect(
				piece_class.PIECE_X_OFFSET, y_offset, 
				PIECE_SIZE_X, PIECE_SIZE_Y
			)

		# Get image for piece
		image = cls.spritesheet.get_image_at(image_position_rect)

		# Initialize graphics for the piece
		piece.init_graphics(image, screen)

		return piece


def remove_square_if_in_possible_moves(
	square: Square, possible_moves: List[Square]
	) -> None:
	if square in possible_moves:
		possible_moves.remove(square)


################################
######### BASE CLASSES #########
################################


class RenderablePiece(Renderable):
	"""A class that handles the graphics of a chess piece."""
	PIECE_X_OFFSET: int  # this must be re-defined by every child class

	def __init__(self, color: ChessColor, square: Square):
		"""Initialize a piece with a color, square, and image and rect."""
		self.color = color
		self.square = square

		# Load image and get its rect - this is done in the create_piece function
		self.image: pg.Surface
		self.rect: pg.Rect

	# Graphics methods
	def init_graphics(self, image: pg.Surface, screen: pg.Surface):
		"""Initialize graphics-related variables and center the piece."""
		self.image = image
		self.rect = self.image.get_rect()

		self.center_in_square(screen)

	def render(self, surface: pg.Surface) -> None:
		"""Renders the piece to the screen."""
		surface.blit(self.image, self.rect)

	def center_in_square(self, surface: pg.Surface):
		"""Center the piece in its square."""
		square_pos = self.square.get_pos(surface)
		self.rect.centerx = square_pos[0] + Square.SQUARE_SIZE // 2
		self.rect.centery = square_pos[1] + Square.SQUARE_SIZE // 2

	def set_pos(self, x: float, y: float):
		"""Set the position of the piece on the screen."""
		self.rect.centerx = x
		self.rect.centery = y

	# String methods
	def __str__(self):
		"""String representation of the piece."""
		colorname = 'Light' if self.color == ChessColor.LIGHT else 'Dark'
		return f'{colorname} {self.__class__} on {self.square.coordinates}'

	def __repr__(self):
		return str(self)


class BasePiece(RenderablePiece):
	"""The base piece class. Represents a piece on the chessboard."""
	# TODO: Instead of storing a reference for a piece's square,
	# store a piece reference in every square.

	# Constants
	PIECE_DICT = {
		'Pawn': 'p', 'Knight': 'n', 'Bishop': 'b',
		'Rook': 'r', 'Queen': 'q', 'King': 'k'
	}

	# Directions for move generation
	HORIZONTAL_DIRECTIONS = (Direction.LEFT, Direction.RIGHT)
	VERTICAL_DIRECTIONS = (Direction.FORWARD, Direction.BACK)

	# Class attributes
	points: int  # how much the piece is worth
	notation: str  # how the piece is represented in chess notation

	# Chess-related methods
	def move_piece(self, move_square: Square, surface: pg.Surface) -> None:
		"""Relocate the piece to a new square and center the piece's rect."""
		self.square = move_square

		self.center_in_square(surface)

	@abstractmethod
	def get_possible_moves(self, board: 'Board') -> List[Square]:
		"""Get the valid squares the piece can move to."""
		raise NotImplemented

	def get_attacked_squares(self, board: 'Board') -> List[Square]:
		"""
		Get the attacked squares of the piece.

		By default this piece returns all the possible moves of the piece,
		but this method exists for detecting pawn attacks, therefore every
		piece has this method.
		"""
		return self.get_possible_moves(board)

	def add_move(
		self, board_squares: List[Square], possible_moves: List[Square], 
		*directions: Direction
		):
		"""
		Add a square to the possible squares list by adding up the directions. 
		Keep in mind that this does not account for pieces on the way to said
		square (like a knight). 
		"""
		kls = self.__class__

		horizontal_increment = 0
		vertical_increment = 0

		# TODO: move these class variables to chess_constants.py
		for direction in directions:
			if direction in kls.HORIZONTAL_DIRECTIONS:
				horizontal_increment += direction.value * self.color.value
			elif direction in kls.VERTICAL_DIRECTIONS:
				vertical_increment += direction.value * self.color.value

		horizontal_validity = self._check_can_move_horizontal(horizontal_increment)
		vertical_validity = self._check_can_move_vertical(vertical_increment)

		can_move_there = horizontal_validity and vertical_validity

		if can_move_there:
			total_increment = horizontal_increment + vertical_increment
			new_square_index = self.square.index + total_increment

			possible_moves.append(board_squares[new_square_index])

	def _check_can_move_horizontal(self, direction_increment: int) -> bool:
		"""Check if the piece can move in a certain horizontal direction."""
		index = self.square.index

		row_current = index // 8
		row_after = (index + direction_increment) // 8

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

	@staticmethod
	def get_directions() -> Tuple[Direction, Direction, Direction, Direction]:
		"""Get the move directions in the order; Forward, back, right, left."""
		return Direction.FORWARD, Direction.BACK, Direction.RIGHT, Direction.LEFT

	def get_number_directions(self) -> Tuple[int, int, int, int]:
		"""
		Get the move directions as in square differences 
		in the order; Forward, back, right, left.
		"""
		number_directions = (d.value*self.color.value for d in self.get_directions())

		return number_directions

	def irow(self, inc: int = 0) -> int:
		"""Return the row of the piece as an integer between 0 and 7."""
		return (self.square.index+inc) // 8

	def icol(self, inc: int = 0) -> int:
		"""Return the column of the piece as an integer between 0 and 7."""
		return (self.square.index+inc) % 8


################################
######### CHESS PIECES #########
################################


class FirstMovePiece(BasePiece):
	"""Pieces that have special first moves."""

	def __init__(self, *args, **kwargs):
		"""Initialize the piece with a boolean has_moved attribute."""
		super().__init__(*args, **kwargs)
		self.has_moved: bool = False


class Pawn(FirstMovePiece):
	"""Represents a pawn on the chessboard."""
	PIECE_X_OFFSET = PIECE_SIZE_X*5
	points = 1
	notation = 'P'  # used for graphics
	PROMOTION_CHOICES = ['Queen', 'Rook', 'Bishop', 'Knight']

	def get_possible_moves(self, board):
		"""Generate the possible moves for a pawn, including captures."""
		# TODO: Promotions
		# TODO: En-passant
		possible_moves = []
		i = self.square.index

		# Get the forward direction value
		forward: int = Direction.FORWARD.value*self.color.value

		# First of all, check if the pawn can move forward.
		if self._check_can_move_vertical(forward):
			# One square forward
			move_square = board.squares[i + forward]
			piece_in_front_of_me = board.get_piece_occupying_square(move_square)

			if piece_in_front_of_me is None:
				if self._check_can_move_vertical(forward):
					possible_moves.append(move_square)

			# Two squares forward
			if not self.has_moved and piece_in_front_of_me is None:
				move_square = board.squares[i + 2*forward]

				if board.get_piece_occupying_square(move_square) is None:
					possible_moves.append(move_square)

			# Get left and right direction values to be used for captures
			left: int = Direction.LEFT.value * self.color.value
			right: int = Direction.RIGHT.value * self.color.value

			# Left diagonal capture
			if self._check_can_move_horizontal(left):
				capture_square = board.squares[i + forward + left]
				occupying_piece = board.get_piece_occupying_square(capture_square)

				if occupying_piece is not None and occupying_piece.color != self.color:
					possible_moves.append(capture_square)

			# Right diagonal capture
			if self._check_can_move_horizontal(right):
				capture_square = board.squares[i + forward + right]
				occupying_piece = board.get_piece_occupying_square(capture_square)

				if occupying_piece is not None and occupying_piece.color != self.color:
					possible_moves.append(capture_square)

		return possible_moves

	def get_attacked_squares(self, board):
		possible_moves = self.get_possible_moves(board)

		# A pawn doesn't "attack" the squares in front
		forward = Direction.FORWARD.value*self.color.value
		one_square_up = self.square.index + forward
		two_squares_up = one_square_up + forward

		remove_square_if_in_possible_moves(one_square_up, possible_moves)
		remove_square_if_in_possible_moves(two_squares_up, possible_moves)

		return possible_moves


class Rook(FirstMovePiece):
	"""Represents a rook on the chessboard."""
	PIECE_X_OFFSET = PIECE_SIZE_X*2
	points = 5
	notation = 'R'

	def get_possible_moves(self, board):
		"""Generate moves for a rook, keeping the blocking pieces in mind."""
		possible_moves = []
		index = self.square.index

		# Get the directions with square index differences.
		f, b, r, l = self.get_number_directions()

		# Create flags to check if we should keep generating moves in that direction.
		generate_fwd, generate_bwd, generate_right, generate_left = True, True, True, True

		for i in range(1, 8):  # loop between 1-7
			# Forward
			if generate_fwd:
				fwd_increment = f*i

				if self._check_can_move_vertical(fwd_increment):
					move_square = board.squares[index + fwd_increment]

					occupying_piece = board.get_piece_occupying_square(move_square)

					if occupying_piece is None:
						possible_moves.append(move_square)
					else:
						possible_moves.append(move_square)
						generate_fwd = False

			# Backward
			if generate_bwd:
				bwd_increment = b*i

				if self._check_can_move_vertical(bwd_increment):
					move_square = board.squares[index + bwd_increment]

					occupying_piece = board.get_piece_occupying_square(move_square)

					if occupying_piece is None:
						possible_moves.append(move_square)
					else:
						possible_moves.append(move_square)
						generate_bwd = False

			# Right
			if generate_right:
				right_increment = r*i

				if self._check_can_move_horizontal(right_increment):
					move_square = board.squares[index + right_increment]

					occupying_piece = board.get_piece_occupying_square(move_square)

					if occupying_piece is None:
						possible_moves.append(move_square)
					else:
						possible_moves.append(move_square)
						generate_right = False

			# Left
			if generate_left:
				left_increment = l*i

				if self._check_can_move_horizontal(left_increment):
					move_square = board.squares[index + left_increment]

					occupying_piece = board.get_piece_occupying_square(move_square)

					if occupying_piece is None:
						possible_moves.append(move_square)
					else:
						possible_moves.append(move_square)
						generate_left = False

		return possible_moves


class King(FirstMovePiece):
	"""Represents a king on the chessboard."""
	PIECE_X_OFFSET = PIECE_SIZE_X*0
	notation = 'K'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Declare the castling rights variables here
		self.fen_kingside_right: bool
		self.fen_queenside_right: bool

	def init_fen_castling_rights(self, castling_rights: str) -> None:
		"""Initializes the castling rights for the king from the entered FEN."""
		if 'k' in castling_rights.lower():
			self.fen_kingside_right = True
		else:
			self.fen_kingside_right = False

		if 'q' in castling_rights.lower():
			self.fen_queenside_right = True
		else:
			self.fen_queenside_right = False

	def get_castling_rights(self, board: 'Board', for_fen=True) -> str:
		if self.has_moved:
			return ""

		castling_rights = ""

		if self.fen_kingside_right:
			if self.can_castle_kingside(board, for_fen=for_fen):
				castling_rights += 'K'

		if self.fen_queenside_right:
			if self.can_castle_queenside(board, for_fen=for_fen):
				castling_rights += 'Q'

		return castling_rights

	def get_possible_moves(self, board):
		possible_moves = []

		# Get directions
		f, b, r, l = self.get_directions()

		# Forward moves
		self.add_move(board.squares, possible_moves, f)
		self.add_move(board.squares, possible_moves, f, r)
		self.add_move(board.squares, possible_moves, f, l)

		# Backward moves
		self.add_move(board.squares, possible_moves, b)
		self.add_move(board.squares, possible_moves, b, r)
		self.add_move(board.squares, possible_moves, b, l)

		# Horizontal moves
		self.add_move(board.squares, possible_moves, r)
		self.add_move(board.squares, possible_moves, l)

		# Castling moves - The rook will be moved in the 'Move' class.
		if not self.has_moved:
			# Reverse directions if it's a black king
			if self.color == ChessColor.DARK:
				previous_l = l
				l = r
				r = previous_l

			# Queenside castling
			if self.can_castle_queenside(board):
				self.add_move(board.squares, possible_moves, l, l)

			# Kingside castling
			if self.can_castle_kingside(board):
				self.add_move(board.squares, possible_moves, r, r)

		return possible_moves

	def can_castle_queenside(self, board: 'Board', for_fen=False) -> bool:
		"""Checks if the king can castle queenside."""
		# Check if the entered FEN grants this castling right
		if not self.fen_queenside_right:
			return False

		# If there are pieces in the way, cancel move generation.
		l = Direction.LEFT.value
		index = self.square.index

		for i in range(1, 4):  # loops between 1-3
			l_increment = l*i
			next_square = board.squares[index + l_increment]
			if board.get_piece_occupying_square(next_square) is not None:
				# There are pieces in the way, cannot castle.
				if not for_fen:
					return False

		# 4 squares left
		return self._can_castle(board, 4*l)

	def can_castle_kingside(self, board: 'Board', for_fen=False) -> bool:
		"""Checks if the king can castle kingside."""
		# Check if the entered FEN grants this castling right
		if not self.fen_kingside_right:
			return False

		# If there are pieces in the way, cancel move generation.
		r = Direction.RIGHT.value
		index = self.square.index

		for i in range(1, 3):  # loops between 1-2
			r_increment = r*i
			next_square = board.squares[index + r_increment]
			if board.get_piece_occupying_square(next_square) is not None:
				# There are pieces in the way, cannot castle.
				if not for_fen:
					return False

		# 3 squares right
		return self._can_castle(board, 3*r)

	def _can_castle(self, board: 'Board', increment: int) -> bool:
		"""Implements the castling right logic."""
		# Get the rook to castle with.
		rook_square = board.squares[self.square.index + increment]
		rook = board.get_piece_occupying_square(rook_square)

		if not rook.__class__ == Rook:
			# The piece is not even a rook
			return False

		if rook is not None:
			if not rook.has_moved:
				# The rook hasn't moved, we can castle.
				return True
			else:
				# The rook has moved, we cannot castle.
				return False
		else:
			# The rook is not where it should be for us to castle!
			return False


class Knight(BasePiece):
	"""Represents a knight on the chessboard."""
	PIECE_X_OFFSET = PIECE_SIZE_X*4
	points = 3
	notation = 'N'

	def get_possible_moves(self, board):
		"""Generate the possible moves for the piece."""
		possible_moves = []

		# Get directions
		f, b, r, l = self.get_directions()

		# Forward moves
		self.add_move(board.squares, possible_moves, f, f, r)
		self.add_move(board.squares, possible_moves, f, f, l)

		# Right moves
		self.add_move(board.squares, possible_moves, r, r, f)
		self.add_move(board.squares, possible_moves, r, r, b)

		# Back moves
		self.add_move(board.squares, possible_moves, b, b, r)
		self.add_move(board.squares, possible_moves, b, b, l)

		# Left moves
		self.add_move(board.squares, possible_moves, l, l, f)
		self.add_move(board.squares, possible_moves, l, l, b)

		return possible_moves


class Bishop(BasePiece):
	"""Represents a bishop on the chessboard."""
	PIECE_X_OFFSET = PIECE_SIZE_X*3
	points = 3
	notation = 'B'

	def get_possible_moves(self, board):
		possible_moves = []
		index = self.square.index

		# Get the directions with square index differences.
		f, b, r, l = self.get_number_directions()

		# Create flags to check if we should keep generating moves in that direction.
		generate_rf, generate_rb, generate_lf, generate_lb = True, True, True, True

		for i in range(1, 8):  # loop between 1-7
			f_increment = f*i
			b_increment = b*i
			r_increment = r*i
			l_increment = l*i

			can_move_f = self._check_can_move_vertical(f_increment)
			can_move_b = self._check_can_move_vertical(b_increment)
			can_move_r = self._check_can_move_horizontal(r_increment)
			can_move_l = self._check_can_move_horizontal(l_increment)

			# Right forward
			if generate_rf:
				if can_move_r and can_move_f:
					move_square = board.squares[index + r_increment + f_increment]

					occupying_piece = board.get_piece_occupying_square(move_square)

					if occupying_piece is None:
						possible_moves.append(move_square)
					else:
						possible_moves.append(move_square)
						generate_rf = False

			# Right backward
			if generate_rb:
				if can_move_r and can_move_b:
					move_square = board.squares[index + r_increment + b_increment]

					occupying_piece = board.get_piece_occupying_square(move_square)

					if occupying_piece is None:
						possible_moves.append(move_square)
					else:
						possible_moves.append(move_square)
						generate_rb = False

			# Left forward
			if generate_lf:
				if can_move_l and can_move_f:
					move_square = board.squares[index + l_increment + f_increment]

					occupying_piece = board.get_piece_occupying_square(move_square)

					if occupying_piece is None:
						possible_moves.append(move_square)
					else:
						possible_moves.append(move_square)
						generate_lf = False

			# Left backward
			if generate_lb:
				if can_move_l and can_move_b:
					move_square = board.squares[index + l_increment + b_increment]

					occupying_piece = board.get_piece_occupying_square(move_square)

					if occupying_piece is None:
						possible_moves.append(move_square)
					else:
						possible_moves.append(move_square)
						generate_lb = False

		return possible_moves


class Queen(Bishop, Rook):
	"""Represents a queen on the chessboard."""
	PIECE_X_OFFSET = PIECE_SIZE_X*1
	points = 9
	notation = 'Q'

	def get_possible_moves(self, board):
		bishop_moves = Bishop.get_possible_moves(self, board)
		rook_moves = Rook.get_possible_moves(self, board)

		return bishop_moves + rook_moves

	def get_attacked_squares(self, board):
		bishop_attacks = Bishop.get_attacked_squares(self, board)
		rook_attacks = Rook.get_attacked_squares(self, board)

		return bishop_attacks + rook_attacks
