from typing import Tuple

from sys import exit as sysexit
import pygame as pg

from constants import *
from board import Board


class Game:
	"""The class that represents the whole application."""

	def __init__(self):
		"""Initialize pygame, the screen and the board."""
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_PROPERTIES)
		pg.display.set_caption(WINDOW_TITLE)

		pg.font.init()
		self.board = Board()

	def start(self):
		"""Start the main loop of the game."""
		while True:
			self.poll_events()
			self.update_screen()

	def poll_events(self):
		"""Check events regarding the pygame window."""
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sysexit(1)

	def update_screen(self):
		"""Draw/render objects to the screen."""
		self.screen.fill(BACKGROUND_COLOR)

		self.board.render(self.screen)

		pg.display.flip()
