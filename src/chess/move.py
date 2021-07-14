# Type annotations
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
	from .board import Board
	from .square import Square

# Sound-related imports
from settings import SOUND_DIR
from pygame import mixer
mixer.init()

# Chess imports
from .chess_constants import ChessColor, Direction
from .piece import BasePiece, FirstMovePiece, King


class Move:
	INVALID_MOVE_SOUND = mixer.Sound(SOUND_DIR / 'invalid_move.wav')

	def __init__(self, to: 'Square', moving_piece: 'BasePiece', occupying_piece: 'BasePiece'):
		"""
		Initialize a move with a the square to move to, the moving
		piece and the occupant of the square the piece is moving to.
		"""
		self.to = to
		self.moving_piece = moving_piece
		self.occupying_piece = occupying_piece

	# Checks (Not as in chess checks :))
	def _check_first_move_piece(self, piece_type):
		if issubclass(piece_type, FirstMovePiece):
			self.moving_piece.has_moved = True

	def _check_capture(self, pieces_list: List['BasePiece']) -> None:
		"""Check if a piece is being captured."""
		if self.moving_piece != self.occupying_piece is not None:
			pieces_list.remove(self.occupying_piece)

	def _check_move_turn(self, move_turn: 'ChessColor') -> bool:
		"""Check if it is the moving piece's _draw_color's turn."""
		if move_turn != self.moving_piece.color:
			return False

		return True

	def _check_same_color(self) -> bool:
		"""Check if the moving piece and the occupying of the move square is the same color."""
		if self.occupying_piece is not None:
			if self.moving_piece.color == self.occupying_piece.color:
				return False

		return True

	def is_valid(self, move_turn: 'ChessColor', possible_squares: List['Square']) -> bool:
		"""Check the validity of the move."""
		# TODO: Validate checks

		if not self._check_move_turn(move_turn):
			# Cannot move if its not your turn
			return False

		if not self._check_same_color():
			# A piece of the same color cannot be captured
			return False

		if type(self.occupying_piece) == King:
			# The king cannot be captured
			return False

		if self.to not in possible_squares:
			# The piece cannot even go there
			return False

		return True

	def make_move(self, board: 'Board', possible_squares: List['Square']) -> None:
		"""Make the move on the board, if it is valid."""
		# TODO: Return notation for the move.
		# TODO: Cannot pass through squares that would put the king in check.

		if self.is_valid(board.move_turn, possible_squares):
			# Check if a piece was captured
			self._check_capture(board.pieces)

			piece_type = self.moving_piece.__class__

			# Check if the king is castling.
			if piece_type == King:
				index_difference = self._get_index_difference()
				index = self.moving_piece.square.index

				# Get left's square index difference
				l_inc = Direction.LEFT.value * self.moving_piece.color.value
				r_inc = Direction.RIGHT.value * self.moving_piece.color.value

				if index_difference == l_inc*2:
					# The king is castling queenside, get the queenside rook.
					qr_square_index = index + l_inc*4
					queenside_rook = board.get_piece_occupying_square(
							board.squares[qr_square_index]
						)

					# Move the rook
					queenside_rook.square = board.squares[index + l_inc]
					queenside_rook.center_in_square(board.surface)
				elif index_difference == r_inc*2:
					# The king is castling kingside, get the kingside rook
					kr_square_index = index + r_inc*3
					kingside_rook = board.get_piece_occupying_square(
							board.squares[kr_square_index]
						)

					# Move the rook
					kingside_rook.square = board.squares[index + r_inc]
					kingside_rook.center_in_square(board.surface)

			# Check if the moving piece is of type 'FirstMovePiece'.
			self._check_first_move_piece(piece_type)

			# Unhighlight the previous square
			self.moving_piece.square.unhighlight()

			# Change the piece's square
			self.moving_piece.square = self.to

			# Change the move turn
			board.move_turn = ChessColor.negate(self.moving_piece.color)
		else:
			# Play the invalid move sound
			Move.INVALID_MOVE_SOUND.play()

			# Unhighlight the current square
			self.moving_piece.square.unhighlight()

		# Center the piece in the square so that it looks nice
		self.moving_piece.center_in_square(board.surface)

	def _get_index_difference(self) -> int:
		return self.to.index - self.moving_piece.square.index
