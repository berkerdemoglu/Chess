from typing import Union

from sys import exit as sysexit
import pygame as pg
import time

# My modules
from constants import (
	SCREEN_PROPERTIES, WINDOW_TITLE,
	BACKGROUND_COLOR, FPS
)
from board import Board
from square import Square
from piece import BasePiece
from move import Move
from utils import time_ms, get_dragged_piece, get_release_square


class Game:
	"""The class that represents the whole application."""

	def __init__(self):
		"""Initialize pygame, the screen and the board."""
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_PROPERTIES)
		pg.display.set_caption(WINDOW_TITLE)

		pg.font.init()
		self.board = Board(self.screen)

		# Flags
		self.dragging_piece: Union[BasePiece, None] = None

	def start(self) -> None:
		"""Start the main loop of the game."""
		update_frequency = 1000000000 / FPS
		delta = 0
		drawn_frames = 0

		now_nano: int
		last_nano = time.time_ns()
		second_counter = time_ms()

		while True:
			now_nano = time.time_ns()
			delta += (now_nano - last_nano) / update_frequency
			last_nano = now_nano

			while delta >= 1:
				self.poll_events()
				self.update()
				delta -= 1
				self.render()
				drawn_frames += 1

			if time_ms() - second_counter > 1000:
				second_counter += 1000
				pg.display.set_caption(f'{WINDOW_TITLE} - {drawn_frames}fps')
				drawn_frames = 0

	def poll_events(self) -> None:
		"""Check events regarding the pygame window."""
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sysexit(1)  # exit the application
			elif event.type == pg.MOUSEBUTTONDOWN:
				self.dragging_piece = get_dragged_piece(self.board)
			elif event.type == pg.MOUSEBUTTONUP:
				if self.is_dragging:
					to_square = get_release_square(self.board)
					self.move_piece(to_square)

					self.dragging_piece = None  # reset flag after making the move

	def move_piece(self, to_square: Square):
		if to_square is not None:
			occupying_piece = self.board.get_piece_occupying_square(to_square)

			move = Move(to_square, self.dragging_piece, occupying_piece)
			move.make_move(self.screen, self.board.pieces)
			del move
		else:
			self.dragging_piece.center_in_square(self.screen)

	@property
	def is_dragging(self) -> bool:
		return True if self.dragging_piece is not None else False

	def render(self) -> None:
		"""Draw/render objects to the screen."""
		self.screen.fill(BACKGROUND_COLOR)

		self.board.render(self.screen)

		pg.display.flip()

	def update(self) -> None:
		"""Update the game."""
		if self.dragging_piece is not None:
			x, y = pg.mouse.get_pos()
			self.dragging_piece.set_pos(x, y)
