from typing import Union

from sys import exit as sysexit
import pygame as pg

# My modules
from base import BaseDisplay
from constants import (
	SCREEN_PROPERTIES, WINDOW_TITLE,
	BACKGROUND_COLOR, FPS
)
from board import Board
from square import Square
from piece import BasePiece
from move import Move
from utils import get_dragged_piece, get_release_square


class ChessGame(BaseDisplay):
	"""The class that represents the game."""

	def __init__(self):
		"""Initialize pygame, the screen and the board."""
		super().__init__(SCREEN_PROPERTIES, WINDOW_TITLE, FPS, BACKGROUND_COLOR)

		pg.font.init()
		self.board = Board(self.screen)

		# Flags
		self.dragged_piece: Union[BasePiece, None] = None

	def move_piece(self, to_square: Square) -> None:
		"""Move the dragged piece to a new square."""
		if to_square is not None:
			occupying_piece = self.board.get_piece_occupying_square(to_square)

			move = Move(to_square, self.dragged_piece, occupying_piece)
			move.make_move(self.board)
			del move
		else:
			self.dragged_piece.square.unhighlight()
			self.dragged_piece.center_in_square(self.screen)

	@property
	def is_dragging(self) -> bool:
		"""Flag for checking if a piece is actually being dragged by the user/player."""
		return True if self.dragged_piece is not None else False

	# Define abstract methods from BaseDisplay below
	def poll_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				# Exit the application.
				sysexit(1)
			elif event.type == pg.MOUSEBUTTONDOWN:
				# Start dragging a piece if it was clicked on.
				self.dragged_piece = get_dragged_piece(self.board)
				if self.dragged_piece is not None:
					self.dragged_piece.square.highlight(Square.CURRENT_SQUARE_HIGHLIGHT)
			elif event.type == pg.MOUSEBUTTONUP:
				# Release the piece being dragged if it exists.
				if self.is_dragging:
					to_square = get_release_square(self.board)
					self.move_piece(to_square)

					# Reset dragged piece reference after making the move
					self.dragged_piece = None

	def render(self):
		super().render()

		self.board.render(self.dragged_piece)

	def update(self):
		if self.dragged_piece is not None:
			x, y = pg.mouse.get_pos()
			self.dragged_piece.set_pos(x, y)
