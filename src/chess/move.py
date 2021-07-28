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
		if not self._check_move_turn(move_turn):
			# Cannot move if its not your turn
			return False

		if not self._check_same_color():
			# A piece of the same color cannot be captured
			return False

		if self.to not in possible_squares:
			# The piece cannot even go there
			return False

		return True

	def check_checks(self, board: 'Board') -> bool:
		# Make the move regardless of whether it can be made or not
		original_square = self.moving_piece.square
		self.moving_piece.square = self.to

		del board.piece_dict[original_square]
		board.piece_dict[self.moving_piece.square] = self.moving_piece

		# Get a list of all attacked squares by the opposite color
		attacked_squares = set()

		for piece in board.pieces:
			if piece.color != self.moving_piece.color:
				piece_moves = piece.get_attacked_squares(board)

				attacked_squares.update(piece_moves)

		# Get the king of the moving color's king.
		king = board.get_pieces(King, self.moving_piece.color)[0]

		# Return false if the king can be captured
		check_validity = not king.square in attacked_squares

		# Undo the move.
		del board.piece_dict[self.moving_piece.square]
		self.moving_piece.square = original_square
		board.piece_dict[self.moving_piece.square] = self.moving_piece

		return check_validity

	def check_castling(self, board: 'Board') -> None:
		"""Check if the king is castling."""
		# TODO: Make sure the king is not passing through attacked squares
		index_difference = self._get_index_difference()
		index = self.moving_piece.square.index

		# Get left's square index difference
		l_inc = Direction.LEFT.value
		r_inc = Direction.RIGHT.value

		if index_difference == l_inc*2:
			# The king is castling queenside
			self._move_castling_rook(board, index, l_inc, 4)
		elif index_difference == r_inc*2:
			# The king is castling kingside
			self._move_castling_rook(board, index, r_inc, 3)

	def _get_index_difference(self) -> int:
		"""Get the index difference of the moving piece's square and the
		square the piece is moving to.""" 
		return self.to.index - self.moving_piece.square.index

	@staticmethod
	def _move_castling_rook(
		board: 'Board', index: int, increment: int, multiply_by: int
		) -> None:
		"""Move the rook the king is castling with."""
		# Get the rook
		rook_square_index = index + increment*multiply_by
		rook = board.get_piece_occupying_square(board.squares[rook_square_index])

		# Move the rook
		rook.move_piece(board.squares[index + increment], board.surface)

	def make_move(self, board: 'Board', possible_squares: List['Square']) -> None:
		"""Make the move on the board, if it is valid."""
		# TODO: Return notation for the move.
		# TODO: Cannot pass through squares that would put the king in check.

		if self.is_valid(board.move_turn, possible_squares) and self.check_checks(board):
			# Check if a piece was captured
			self._check_capture(board.pieces)

			piece_type = self.moving_piece.__class__

			# Check if the king is castling
			if piece_type == King:
				self.check_castling(board)

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

		# Update the piece dict of the board.
		board.update_piece_dict()

	def __str__(self):
		return f'<Move: {self.moving_piece} moving to {self.to}>'

	def __repr__(self):
		return str(self)
