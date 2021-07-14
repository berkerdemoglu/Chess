# Type annotations
from typing import Union, TYPE_CHECKING, List
if TYPE_CHECKING:
	from chess.piece import BasePiece

# Pygame and system
from sys import exit as sysexit
import pygame as pg

# My utilities
from graphics import Display
from graphics import (
	SCREEN_PROPERTIES, WINDOW_TITLE,
	BACKGROUND_COLOR, FPS
)
from utils import get_dragged_piece, get_release_square

# Chess imports
from chess import Board, Move, Square
from fen_parser.board_parser import BoardParser


class ChessGame(Display):
	"""The class that represents the game."""

	def __init__(self, fen_str: str = Board.DEFAULT_POSITION_FEN):
		"""Initialize pygame, the screen and the board."""
		super().__init__(SCREEN_PROPERTIES, WINDOW_TITLE, FPS, BACKGROUND_COLOR)

		self.board: Board = Board(self.screen, fen_str)
		self.board_parser: BoardParser = BoardParser(self.board)

		# Flags
		self.dragged_piece: Union['BasePiece', None] = None
		self.possible_squares: Union['List', None] = None

	def move_piece(self, to_square: 'Square') -> None:
		"""Move the dragged piece to a new square."""
		if to_square is not None:
			# Get the current occupant of the square to piece is trying to move to.
			occupying_piece = self.board.get_piece_occupying_square(to_square)

			# Create a move and make it.
			move = Move(to_square, self.dragged_piece, occupying_piece)
			move.make_move(self.board, self.possible_squares)

			# Delete now useless objects to free up memory.
			del move
		else:
			self.dragged_piece.square.unhighlight()
			self.dragged_piece.center_in_square(self.screen)

		# Unhighlight all previously highlighted squares.
		for square in self.possible_squares:
			square.unhighlight()

	@property
	def is_dragging(self) -> bool:
		"""Flag for checking if a piece is actually being dragged by the user/player."""
		return True if self.dragged_piece is not None else False

	@is_dragging.setter
	def is_dragging(self, value) -> None:
		self.dragged_piece = value

	# Define abstract methods from Display below
	def poll_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				# Exit the application.
				sysexit(1)
			elif event.type == pg.MOUSEBUTTONDOWN:
				# Start dragging a piece if it was clicked on.
				self.dragged_piece = get_dragged_piece(self.board)
				if self.dragged_piece is not None:
					# Highlight the dragged piece's current square.
					self.dragged_piece.square.highlight(Square.CURRENT_SQUARE_HIGHLIGHT)

					# Get possible squares the piece can move to.
					self.possible_squares = self.dragged_piece.get_possible_moves(self.board)
			elif event.type == pg.MOUSEBUTTONUP:
				# Release the piece being dragged if it exists.
				if self.is_dragging:
					to_square = get_release_square(self.board)
					self.move_piece(to_square)

					# Reset dragged piece reference after making the move
					self.is_dragging = None

	def render(self):
		super().render()

		self.board.render(self.dragged_piece)

	def update(self):
		if self.dragged_piece is not None:
			x, y = pg.mouse.get_pos()
			self.dragged_piece.set_pos(x, y)
