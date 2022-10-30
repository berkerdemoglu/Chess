# Type annotations
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
	from chess import Board, Square
	from chess.piece import BasePiece

import pygame as pg
from time import time as time_now


def sort_word_by_case(word: str) -> Tuple[str, str]:
	uppercase_letters = ""
	lowercase_letters = ""

	for ch in word:
		if ch.isupper():
			uppercase_letters += ch
		else:
			lowercase_letters += ch

	return uppercase_letters, lowercase_letters


def blend_colors(
		rgba: Tuple[int, int, int, float], rgb: Tuple[int, int, int]
	) -> Tuple[int, int, int]:
	"""Get the resulting RGB color of an RGBA color rendered over an RGB color."""
	red = (rgba[0] * rgba[3]) + (rgb[0] * (1 - rgba[3]))
	blue = (rgba[1] * rgba[3]) + (rgb[1] * (1 - rgba[3]))
	green = (rgba[2] * rgba[3]) + (rgb[2] * (1 - rgba[3]))
	result_color = int(red), int(blue), int(green)
	return result_color


# Used for calculating the FPS
def time_ms():
	"""Return the current time in milliseconds."""
	return round(time_now() * 1000)


# Move-related functions
def get_dragged_piece(board: 'Board') -> 'BasePiece':
	"""Get the dragged piece by the mouse's current coordinates."""
	mouse_x, mouse_y = pg.mouse.get_pos()
	return board.get_piece_by_coords(mouse_x, mouse_y)


def get_release_square(board: 'Board') -> 'Square':
	"""Get the square where the piece was released."""
	mouse_x, mouse_y = pg.mouse.get_pos()
	return board.get_square_by_coords(mouse_x, mouse_y)


def point_in_rect(x: int, y: int, rect: pg.Rect) -> bool:
	"""Check if a point is in a rect."""
	rect_x1, rect_y1, width, height = rect
	rect_x2 = rect_x1 + width
	rect_y2 = rect_y1 + height

	if rect_x1 <= x <= rect_x2 and rect_y1 <= y <= rect_y2:
		return True

	return False
