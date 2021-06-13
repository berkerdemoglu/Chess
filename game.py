from typing import Tuple

from sys import exit as sysexit
import pygame as pg

from constants import *
from board import Board


class Game:

	def __init__(self):
		pg.font.init()
		self.board = Board()

	def start(self):
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_PROPERTIES)
		pg.display.set_caption(WINDOW_TITLE)

		while True:
			self.poll_events()
			self.update_screen()

	def poll_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sysexit(1)

	def update_screen(self):
		self.screen.fill(BACKGROUND_COLOR)

		self.board.render(self.screen)

		pg.display.flip()
