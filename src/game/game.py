# Type annotations
from typing import Union, TYPE_CHECKING, List
if TYPE_CHECKING:
	from chess.piece import BasePiece
	from .menu import MenuWidget

# Pygame and system
from sys import exit as sysexit
import pygame as pg

# My utilities
from settings import ASSETS_DIR

from graphics import Display
from graphics import (
	SCREEN_PROPERTIES, WINDOW_TITLE,
	BACKGROUND_COLOR
)
from utils import (
	get_dragged_piece, 
	get_release_square, 
	point_in_rect
)

# Chess imports
from chess import Board, Move, Square, DEFAULT_POSITION_FEN
from fen_parser.board_parser import BoardParser
from .menu import ChessMenu, ChessMenuHandler


class ChessGame(Display):
	"""The class that represents the game."""

	def __init__(self, fen_str: str = DEFAULT_POSITION_FEN):
		"""Initialize pygame, the screen and the board."""
		super().__init__(SCREEN_PROPERTIES, WINDOW_TITLE, BACKGROUND_COLOR)

		# Board
		self.board: Board = Board(self.screen, fen_str)
		self.board_parser: BoardParser = BoardParser(self.board)

		# Chess screen menu
		self.chess_menu: ChessMenu = ChessMenu()
		self.chess_menu_handler: ChessMenuHandler = ChessMenuHandler(self.board_parser)

		# Flags
		self.dragged_piece: Union['BasePiece', None] = None
		self.possible_squares: Union[List, None] = None

		self.pressed_widget: Union['MenuWidget', None] = None

	def move_piece(self, to_square: 'Square') -> None:
		"""Move the dragged piece to a new square."""
		if to_square is not None:
			# Get the current occupant of the square to piece is trying to move to.
			occupying_piece = self.board.get_piece_occupying_square(to_square)

			# Create a move and make it.
			move = Move(to_square, self.dragged_piece, occupying_piece)
			move.make_move(self.board, self.possible_squares)
		else:
			self.dragged_piece.square.unhighlight()
			self.dragged_piece.center_in_square(self.screen)

		# Unhighlight all previously highlighted squares.
		for square in self.possible_squares:
			square.unhighlight()

	# Define abstract methods from Display below
	def poll_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				# Exit the application.
				sysexit(1)
			elif event.type == pg.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pg.mouse.get_pos()
				if point_in_rect(mouse_x, mouse_y, self.board.border_rect):  # Chessboard
					# Start dragging a piece if it was clicked on.
					self.dragged_piece = get_dragged_piece(self.board)
					if self.dragged_piece is not None:
						# Highlight the dragged piece's current square.
						self.dragged_piece.square.highlight(Square.CURRENT_SQUARE_HIGHLIGHT)

						# Get possible squares the piece can move to.
						self.possible_squares = self.dragged_piece.get_possible_moves(self.board)
				else:  # Chess menu
					# Highlight and handle pressed widget if a widget was clicked on.
					self.pressed_widget = self.chess_menu.get_pressed_widget(mouse_x, mouse_y)
					if self.pressed_widget is not None:
						self.chess_menu_handler.handle(self.pressed_widget)
						self.pressed_widget.highlight()
			elif event.type == pg.MOUSEBUTTONUP:
				# Release the piece being dragged if it exists.
				if self.dragged_piece is not None:
					to_square = get_release_square(self.board)
					self.move_piece(to_square)

					# Reset dragged piece reference after making the move
					self.dragged_piece = None

				# Unhighlight the pressed widget if it exists.
				if self.pressed_widget is not None:
					self.pressed_widget.unhighlight()

					# Reset pressed widget reference
					self.pressed_widget = None

	def render(self):
		super().render()
		self.board.render(self.dragged_piece)
		self.chess_menu.render(self.screen)

	def update(self):
		if self.dragged_piece is not None:
			x, y = pg.mouse.get_pos()
			self.dragged_piece.set_pos(x, y)
