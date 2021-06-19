# Typing
from typing import List
from pygame import Surface

from square import Square
from piece import BasePiece, King


class Move:

	def __init__(self, to: Square, moving_piece: BasePiece, occupying_piece: BasePiece):
		"""
		Initialize a move with a the square to move to, the moving
		piece and the occupant of the square the piece is moving to.
		"""
		self.to = to
		self.moving_piece = moving_piece
		self.occupying_piece = occupying_piece

	def _check_capture(self, pieces_list: List[BasePiece]):
		"""Check if a piece is being captured."""
		if self.moving_piece != self.occupying_piece is not None:
			pieces_list.remove(self.occupying_piece)

	def is_valid(self) -> bool:
		"""Check the validity of the move."""
		if self.occupying_piece is not None:
			if self.moving_piece.color == self.occupying_piece.color:
				return False

		if type(self.occupying_piece) == King:
			return False

		return True

	def make_move(self, surface: Surface, pieces_list: List[BasePiece]) -> None:
		"""Make the move on the board, if it is valid."""
		if self.is_valid():
			self._check_capture(pieces_list)
			self.moving_piece.square = self.to

		self.moving_piece.center_in_square(surface)
