from typing import Tuple

import pygame as pg

from base import BaseDrawable
from constants import BLACK, WHITE


class Square(BaseDrawable):
	SQUARE_SIZE = 60

	def __init__(self, color: Tuple[int, int, int], pos: Tuple[int, int]):
		self.color = color
		self._colorname = 'WHITE' if color == WHITE else 'BLACK'

		self.center_x = pos[0]
		self.center_y = pos[1]
		self._center = pos

	def _get_rect(self, surface: pg.Surface) -> pg.Rect:
		surface_rect = surface.get_rect()
		size = Square.SQUARE_SIZE

		x = self.center_x + surface_rect.centerx - 4*size
		y = self.center_y + surface_rect.centery - 4*size

		return pg.Rect(x, y, size, size)

	def render(self, surface: pg.Surface):
		rect = self._get_rect(surface)

		pg.draw.rect(surface, self.color, rect)

	def __str__(self):
		return f'Color: {self._colorname}, Center: {self._center}'
