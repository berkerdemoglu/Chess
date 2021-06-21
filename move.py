# Typing
from typing import List
from pygame import Surface, mixer

from board import Board
from square import Square
from piece import BasePiece, King
from constants import PieceColor, ASSETS_DIR


mixer.init()


class Move:
	INVALID_MOVE_SOUND = mixer.Sound(ASSETS_DIR / 'invalid_move.wav')

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

	def is_valid(self, move_turn: PieceColor) -> bool:
		"""Check the validity of the move."""
		if move_turn != self.moving_piece.color:
			return False

		if self.occupying_piece is not None:
			if self.moving_piece.color == self.occupying_piece.color:
				return False

		if type(self.occupying_piece) == King:
			return False

		return True

	def make_move(self, board: Board) -> None:
		"""Make the move on the board, if it is valid."""
		if self.is_valid(board.move_turn):
			self._check_capture(board.pieces)

			self.moving_piece.square.unhighlight()

			self.moving_piece.square = self.to  # change the piece's square
			board.move_turn = PieceColor.negate(self.moving_piece.color)
		else:
			Move.INVALID_MOVE_SOUND.play()

		self.moving_piece.square.unhighlight()
		self.moving_piece.center_in_square(board.surface)
