# Type annotations
from typing import Tuple, Union, NoReturn

import pygame as pg

from graphics import Renderable
from utils import blend_colors
from .chess_constants import ChessColor


pg.font.init()


__all__ = ['Square']


#############################
######### UTILITIES #########
#############################


def _get_file_str(file: int) -> Union[str, NoReturn]:
	"""Convert a given integer to a file letter on a chessboard."""
	file_dict = {  # Used for int to str lookup for files
		0: 'a', 1: 'b', 2: 'c',
		3: 'd', 4: 'e', 5: 'f',
		6: 'g', 7: 'h'
	}

	return file_dict[file]

def _get_rank_str(rank: int) -> str:
	"""Convert a given integer to a rank number on a chessboard."""
	return str(8 - rank)


############################
##### THE SQUARE CLASS #####
############################


class Square(Renderable):
	"""Represents a single square on the chessboard."""
	SQUARE_SIZE = 75  # size on the screen

	# Colors
	DARK_SQUARE_COLOR = (140, 94, 67)
	LIGHT_SQUARE_COLOR = (247, 237, 205)

	# Highlight colors
	CURRENT_SQUARE_HIGHLIGHT = (255, 222, 33, 0.5)
	MOVED_SQUARE_HIGHLIGHT = (255, 0, 0, 0.5)
	VALID_MOVE_HIGHLIGHT = (53, 116, 204, 0.5)

	# Fonts
	SQUARE_FONT_PROPERTIES = ('monospace', 14)
	SQUARE_FONT = pg.font.SysFont(*SQUARE_FONT_PROPERTIES)
	SQUARE_FONT_COLOR = (32, 30, 31)

	def __init__(
		self, color: ChessColor, pos: Tuple[int, int], 
		index: int, surface: pg.Surface
		):
		"""Initialize the color and the position of the square."""
		self.color = color
		self._draw_color = self._init_draw_color()
		self._highlight_color = self._init_highlight_color()
		self._colorname = 'LIGHT' if color == Square.LIGHT_SQUARE_COLOR else 'DARK'

		self.center_x = pos[0]
		self.center_y = pos[1]
		self._center = pos
		self.rect = self._init_rect(surface)

		self.index = index  # index in the squares list
		self.coordinates = self._init_coordinates()

	def _init_coordinates(self) -> str:
		"""Help initialize the coordinates of the square on a chessboard."""
		file = _get_file_str(int(self._center[0] / Square.SQUARE_SIZE))
		rank = _get_rank_str(int(self._center[1] / Square.SQUARE_SIZE))
		return file + rank

	def _init_draw_color(self) -> Tuple[int, int, int]:
		if self.color == ChessColor.LIGHT:
			return Square.LIGHT_SQUARE_COLOR
		else:
			return Square.DARK_SQUARE_COLOR

	def _init_highlight_color(self) -> Tuple[int, int, int, float]:
		return self._draw_color[0], self._draw_color[1], self._draw_color[2], 1.0

	def _init_rect(self, surface: pg.Surface) -> pg.Rect:
		"""Get the rect of the square, ready to be rendered to the screen."""
		coordinates = self.get_pos(surface)

		return pg.Rect(*coordinates, Square.SQUARE_SIZE, Square.SQUARE_SIZE)

	def get_pos(self, surface: pg.Surface) -> Tuple[int, int]:
		"""Get the coordinates of the square on the screen."""
		surface_rect = surface.get_rect()
		x = self.center_x + surface_rect.centerx - 4*Square.SQUARE_SIZE
		y = self.center_y + surface_rect.centery - 4*Square.SQUARE_SIZE

		return x, y

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
		pg.draw.rect(surface, self.get_render_color(), self.rect)

	def __str__(self):
		"""String representation of a square."""
		return f'Color: {self._colorname}, Coordinates: {self.coordinates}'

	def __repr__(self):
		return str(self)
