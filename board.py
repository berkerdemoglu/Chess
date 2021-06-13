import pygame as pg

from typing import Sequence

from base import BaseDrawable
from constants import WHITE, BLACK
from square import Square


class Board(BaseDrawable):
	
	def __init__(self):
		self.squares = Board._create_board()

		self.font = pg.font.SysFont(*Square.SQUARE_FONT)

	@classmethod
	def _create_board(cls) -> Sequence[Square]:
		squares = []

		for file in range(8):
			for rank in range(7, -1, -1):
				color = Square.LIGHT_SQUARE_COLOR if (file+rank) % 2 == 0 else Square.DARK_SQUARE_COLOR
				pos = (file * Square.SQUARE_SIZE, rank * Square.SQUARE_SIZE)

				square = Square(color, pos)
				squares.append(square)

		return squares

	def render(self, surface):
		for square in self.squares:
			square.render(surface)
			label = self.font.render(square.squarename, 1, Square.SQUARE_FONT_COLOR)
			surface.blit(label, square.get_coordinates(surface))
