from typing import Tuple

import pygame as pg

from base import BaseDrawable


class Square(BaseDrawable):
	"""Represents a single square on the chessboard."""
	SQUARE_SIZE = 75

	DARK_SQUARE_COLOR = (140, 94, 67)
	LIGHT_SQUARE_COLOR = (247, 237, 205)

	SQUARE_FONT = ('monospace', 14)
	SQUARE_FONT_COLOR = (32, 30, 31)

	def __init__(self, color: Tuple[int, int, int], pos: Tuple[int, int], index: int):
		"""Initialize the color and the position of the square."""
		self.color = color
		self._colorname = 'LIGHT' if color == Square.LIGHT_SQUARE_COLOR else 'DARK'

		self.center_x = pos[0]
		self.center_y = pos[1]
		self._center = pos

		self.index = index  # index in the squares list

	@property
	def coordinates(self) -> str:
		"""The coordinates of the square on a typical chessboard."""
		file = self._get_file_str(int(self._center[0] / Square.SQUARE_SIZE))
		rank = self._get_rank_str(int(self._center[1] / Square.SQUARE_SIZE))
		return file + rank

	@staticmethod
	def _get_file_str(file: int):
		"""Convert a given integer to a file letter on a chessboard."""
		if file == 0:
			file_str = 'a'
		elif file == 1:
			file_str = 'b'
		elif file == 2:
			file_str = 'c'
		elif file == 3:
			file_str = 'd'
		elif file == 4:
			file_str = 'e'
		elif file == 5:
			file_str = 'f'
		elif file == 6:
			file_str = 'g'
		elif file == 7:
			file_str = 'h'
		else:
			raise ValueError('File (as an integer) must be between 0 and 7')

		return file_str

	@staticmethod
	def _get_rank_str(rank: int):
		"""Convert a given integer to a rank number on a chessboard."""
		return str(8 - rank)

	def get_coordinates(self, surface: pg.Surface) -> Tuple[int, int]:
		"""Get the coordinates of the square on a chessboard."""
		surface_rect = surface.get_rect()
		x = self.center_x + surface_rect.centerx - 4*Square.SQUARE_SIZE
		y = self.center_y + surface_rect.centery - 4*Square.SQUARE_SIZE

		return x, y

	def get_rect(self, surface: pg.Surface) -> pg.Rect:
		"""Get the rect of the square, ready to be rendered to the screen."""
		coordinates = self.get_coordinates(surface)

		return pg.Rect(*coordinates, Square.SQUARE_SIZE, Square.SQUARE_SIZE)

	def render(self, surface: pg.Surface):
		rect = self.get_rect(surface)

		pg.draw.rect(surface, self.color, rect)

	def __str__(self):
		return f'Color: {self._colorname}, Coordinates: {self.coordinates}'

	def __repr__(self):
		return str(self)
