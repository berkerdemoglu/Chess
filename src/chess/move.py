# Type annotations
from typing import Callable, Sequence, Tuple, List, TYPE_CHECKING
if TYPE_CHECKING:
	from .board import Board
	from .square import Square

# Sound-related imports
import pygame as pg
from settings import ASSETS_DIR

# Import tkinter for pawn promotion GUI
import tkinter as tk

# Chess imports
from .chess_constants import ChessColor, Direction
from .piece import *

# Define what can be imported from this module
__all__ = ['Move']

# Init pygame's sound package
pg.mixer.init()


#################################
######### PROMOTION GUI #########
#################################
def create_choice_button(root: tk.Tk, choice: str, promotion_cmd: Callable) -> tk.Button:
	"""Create a button for the promotion dialog."""
	cmd = lambda: promotion_cmd(choice)
	button = tk.Button(
			root, text=choice, padx=10, pady=10, command=cmd
		)
	return button


class PromotionDialog(tk.Tk):
	"""Represents the dialog that opens when a pawn is being promoted."""

	def __init__(self, choices: Sequence[str]):
		super().__init__()
		self.title('Promote')

		self.buttons = []
		for choice in choices:
			button = create_choice_button(
					self, choice, self._choose_promotion
				)
			self.buttons.append(button)

		self.promotion_choice = None

	def start_dialog(self):
		"""Start the promotion dialog."""
		self.draw_widgets()
		self.mainloop()

	def draw_widgets(self):
		"""Draw the buttons on the dialog."""
		for i in range(len(self.buttons)):
			button = self.buttons[i]
			button.grid(row=0, column=i)

	def _choose_promotion(self, user_choice: str):
		"""Get the promotion that the user chose and close the dialog."""
		self.promotion_choice = user_choice
		self.destroy()


##################################
######### THE MOVE CLASS #########
##################################


class Move:
	"""Represents a move on the chessboard."""
	INVALID_MOVE_SOUND = pg.mixer.Sound(ASSETS_DIR / 'invalid_move.wav')

	def __init__(
			self, to: 'Square', moving_piece: 'BasePiece', 
			occupying_piece: 'BasePiece'
		):
		"""
		Initialize a move with a the square to move to, the moving
		piece and the occupant of the square the piece is moving to.
		"""
		self.to = to
		self.moving_piece = moving_piece
		self.occupying_piece = occupying_piece

	# Checks (Not as in chess checks :))
	def _update_has_moved(self, piece_type):
		"""
		Check if the moving piece has special first moves and if so,
		set the has_moved flag to True, to stop generating those moves.
		"""
		if issubclass(piece_type, FirstMovePiece):
			self.moving_piece.has_moved = True

	def _check_capture(self, pieces_list: List['BasePiece']) -> None:
		"""Remove the piece on the TO square, if it is being captured."""
		if self.occupying_piece is not None:
			pieces_list.remove(self.occupying_piece)

	def _check_move_turn(self, move_turn: 'ChessColor') -> bool:
		"""Check if it is the moving piece's _draw_color's turn."""
		if move_turn != self.moving_piece.color:
			return False

		return True

	def _check_same_color(self) -> bool:
		"""Check if the moving piece and the occupant of the TO square are the same color."""
		if self.occupying_piece is not None:
			if self.moving_piece.color == self.occupying_piece.color:
				return False

		return True

	def is_valid(self, move_turn: 'ChessColor', possible_squares: List['Square']) -> bool:
		"""Check the validity of the move, regarding game logic."""
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

	def _check_checks(self, board: 'Board') -> bool:
		"""Check the validity of the move, regarding chess checks."""
		if self.occupying_piece is not None:
			# if there is a piece on the TO square, capture it
			del board.piece_dict[self.to]

		# Move the piece regardless of whether it is valid or not
		original_square = self.moving_piece.square
		self.moving_piece.square = self.to
		del board.piece_dict[original_square]
		board.piece_dict[self.moving_piece.square] = self.moving_piece

		# Get a list of all attacked squares by the opposite color
		# except the piece on the TO square
		attacked_squares = set()
		for piece in board.pieces:
			if piece.color != self.moving_piece.color and piece != self.occupying_piece:
				piece_moves = piece.get_attacked_squares(board)
				attacked_squares.update(piece_moves)

		# Move is invalid if the moving color's king can be captured
		king = board.get_king(self.moving_piece.color)
		check_validity = not king.square in attacked_squares

		# Undo the move.
		del board.piece_dict[self.moving_piece.square]
		self.moving_piece.square = original_square
		board.piece_dict[self.moving_piece.square] = self.moving_piece
		board.piece_dict[self.to] = self.occupying_piece

		return check_validity

	def _check_castling(self, board: 'Board') -> None:
		"""Check if the king is castling and if so, move the rook."""
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
		rook.move_piece(board.squares[index + increment], board.screen)

	def _check_promotion(self, board: 'Board') -> None:
		"""Promote the pawn, if it is on the last row."""
		# TODO: Add promotion cancelling
		promotion_row = 0 if self.moving_piece.color == ChessColor.LIGHT else 7

		if self.moving_piece.irow(self._get_index_difference()) == promotion_row:
			# The pawn is being promoted, start the promotion dialog
			dialog = PromotionDialog(Pawn.PROMOTION_CHOICES)
			dialog.start_dialog()

			if dialog.promotion_choice is None:
				return
			board.pieces.remove(self.moving_piece)

			# Change the moving piece from pawn to the promotion of choice
			# TODO: Replace eval with something better
			PromotionClass = eval(dialog.promotion_choice)
			self.moving_piece = PieceCreator.create_piece(
					PromotionClass, self.moving_piece.color,
					self.moving_piece.square, board.screen
				)
			board.pieces.append(self.moving_piece)

	def make_move(self, board: 'Board', possible_squares: List['Square']) -> None:
		"""Make the move on the board, if it is valid."""
		# TODO: Return notation for the move.
		# TODO: Implement checkmate and stalemate

		if self.is_valid(board.move_turn, possible_squares) and self._check_checks(board):
			# Check if a piece was captured
			self._check_capture(board.pieces)

			piece_type = self.moving_piece.__class__
			if piece_type == King:
				# Check if the king is castling
				self._check_castling(board)
			elif piece_type == Pawn:
				# Check if a pawn is being promoted
				self._check_promotion(board)

			# Check if the moving piece is of type 'FirstMovePiece'.
			self._update_has_moved(piece_type)

			# Unhighlight the previous square
			self.moving_piece.square.unhighlight()

			# Change the piece's square
			self.moving_piece.square = self.to

			# Change the move turn
			board.move_turn = ChessColor.negate(self.moving_piece.color)

			# Increment move number
			board.increment_move_number()
		else:
			# Play the invalid move sound
			Move.INVALID_MOVE_SOUND.play()

			# Unhighlight the current square
			self.moving_piece.square.unhighlight()

		# Center the piece in the square so that it looks nice
		self.moving_piece.center_in_square(board.screen)

		# Update the piece dict of the board.
		board.update_piece_dict()

	def __str__(self):
		return f'<Move: {self.moving_piece} moving to {self.to}>'

	def __repr__(self):
		return str(self)
