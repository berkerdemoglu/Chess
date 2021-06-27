# Type annotations
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
	from .board import Board
	from .square import Square

from settings import ASSETS_DIR
from .chess_constants import ChessColor
from .piece import BasePiece, King

from pygame import mixer
mixer.init()


class Move:
	INVALID_MOVE_SOUND = mixer.Sound(ASSETS_DIR / 'invalid_move.wav')

	def __init__(self, to: 'Square', moving_piece: 'BasePiece', occupying_piece: 'BasePiece'):
		"""
		Initialize a move with a the square to move to, the moving
		piece and the occupant of the square the piece is moving to.
		"""
		self.to = to
		self.moving_piece = moving_piece
		self.occupying_piece = occupying_piece

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

	def is_valid(self, move_turn: 'ChessColor') -> bool:
		"""Check the validity of the move."""
		if not self._check_move_turn(move_turn):
			return False

		if not self._check_same_color():
			return False

		if type(self.occupying_piece) == King:
			return False

		return True

	def make_move(self, board: 'Board') -> None:
		"""Make the move on the board, if it is valid."""
		if self.is_valid(board.move_turn):
			self._check_capture(board.pieces)

			self.moving_piece.square.unhighlight()  # unhighlight the previous square

			self.moving_piece.square = self.to  # change the piece's square
			board.move_turn = ChessColor.negate(self.moving_piece.color)
		else:
			Move.INVALID_MOVE_SOUND.play()
			self.moving_piece.square.unhighlight()  # unhighlight the current square

		self.moving_piece.center_in_square(board.surface)
