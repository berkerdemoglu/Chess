# Type annotations
from typing import Tuple, Union, NoReturn

import pygame as pg

from base import Renderable
from utils import blend_colors
from .chess_constants import ChessColor


pg.font.init()


class Square(Renderable):
	"""Represents a single square on the chessboard."""
	SQUARE_SIZE = 75  # size on the screen

	# Colors
	DARK_SQUARE_COLOR = (140, 94, 67)
	LIGHT_SQUARE_COLOR = (247, 237, 205)

	# Highlight colors
	CURRENT_SQUARE_HIGHLIGHT = (255, 222, 33, 0.5)
	MOVED_SQUARE_HIGHLIGHT = (255, 0, 0, 0.5)

	# Fonts
	SQUARE_FONT_PROPERTIES = ('monospace', 14)
	SQUARE_FONT = pg.font.SysFont(*SQUARE_FONT_PROPERTIES)

	_FILE_DICT = {  # Used for int to str lookup for files
		0: 'a', 1: 'b', 2: 'c',
		3: 'd', 4: 'e', 5: 'f',
		6: 'g', 7: '8'
	}

	def __init__(self, color: ChessColor, pos: Tuple[int, int], index: int):
		"""Initialize the color and the position of the square."""
		self.color = color
		self._draw_color = Square.LIGHT_SQUARE_COLOR \
			if color == ChessColor.LIGHT else Square.DARK_SQUARE_COLOR
		self._highlight_color: Tuple[int, int, int, float] = \
			self._draw_color[0], self._draw_color[1], self._draw_color[2], 1.0
		self._colorname = 'LIGHT' if color == Square.LIGHT_SQUARE_COLOR else 'DARK'

		self.center_x = pos[0]
		self.center_y = pos[1]
		self._center = pos

		self.index = index  # index in the squares list

	@property
	def coordinates(self) -> str:
		"""The coordinates of the square on a chessboard."""
		file = self._get_file_str(int(self._center[0] / Square.SQUARE_SIZE))
		rank = self._get_rank_str(int(self._center[1] / Square.SQUARE_SIZE))
		return file + rank

	@staticmethod
	def _get_file_str(file: int) -> Union[str, NoReturn]:
		"""Convert a given integer to a file letter on a chessboard."""
		try:
			file_str = Square._FILE_DICT[file]
		except KeyError:
			raise ValueError('File (as an integer) must be between 0 and 7')
		else:
			return file_str

	@staticmethod
	def _get_rank_str(rank: int) -> str:
		"""Convert a given integer to a rank number on a chessboard."""
		return str(8 - rank)

	def get_pos(self, surface: pg.Surface) -> Tuple[int, int]:
		"""Get the coordinates of the square on the screen."""
		surface_rect = surface.get_rect()
		x = self.center_x + surface_rect.centerx - 4*Square.SQUARE_SIZE
		y = self.center_y + surface_rect.centery - 4*Square.SQUARE_SIZE

		return x, y

	def get_rect(self, surface: pg.Surface) -> pg.Rect:
		"""Get the rect of the square, ready to be rendered to the screen."""
		coordinates = self.get_pos(surface)

		return pg.Rect(*coordinates, Square.SQUARE_SIZE, Square.SQUARE_SIZE)

	# Color-related methods
	def highlight(self, highlight_color: Tuple[int, int, int, float]):
		"""Highlight the square with a RGBA color."""
		self._highlight_color = highlight_color

	def unhighlight(self):
		"""Unhighlight the square."""
		self._highlight_color = self._draw_color[0], self._draw_color[1], self._draw_color[2], 1.0

	def get_render_color(self):
		"""Get the square's color for graphics."""
		return blend_colors(self._highlight_color, self._draw_color)

	def render(self, surface: pg.Surface):
		rect = self.get_rect(surface)

		pg.draw.rect(surface, self.get_render_color(), rect)

	def __str__(self):
		"""String representation of a square."""
		return f'Color: {self._colorname}, Coordinates: {self.coordinates}'

	def __repr__(self):
		return str(self)
