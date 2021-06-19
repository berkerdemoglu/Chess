# Typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from board import Board
	from piece import BasePiece
	from square import Square

import pygame as pg
from time import time as time_now


def point_in_rect(x: int, y: int, rect: pg.Rect) -> bool:
	"""Check if a point is in a rect."""
	rect_x1, rect_y1, width, height = rect
	rect_x2 = rect_x1 + width
	rect_y2 = rect_y1 + height

	if rect_x1 <= x <= rect_x2 and rect_y1 <= y <= rect_y2:
		return True

	return False


def time_ms():
	"""Return the current time in milliseconds."""
	return round(time_now() * 1000)


def get_dragged_piece(board: 'Board') -> 'BasePiece':
	"""Get the dragged piece by the mouse's current coordinates."""
	mouse_x, mouse_y = pg.mouse.get_pos()
	return board.get_piece_by_coords(mouse_x, mouse_y)


def get_release_square(board: 'Board') -> 'Square':
	"""Get the square where the piece was released."""
	mouse_x, mouse_y = pg.mouse.get_pos()
	return board.get_square_by_coords(mouse_x, mouse_y)
