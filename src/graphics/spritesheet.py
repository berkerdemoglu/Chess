# Typing
from typing import Union, TYPE_CHECKING
if TYPE_CHECKING:
	from pathlib import Path

import pygame as pg


class Spritesheet:
	"""Handles reading spritesheet and getting images from it."""
	# TODO: convert_alpha()?
	# for piece_x_offset, add position for every piece in the .ini file

	def __init__(self, filename: Union[str, 'Path']):
		"""Load the spritesheet."""
		self.sheet = pg.image.load(filename)

	def get_image_at(self, rect: pg.Rect):
		"""Get the image that is covered by the given Rect."""
		image = pg.Surface(rect.size, pg.SRCALPHA)
		image.blit(self.sheet, (0, 0), rect)
		image.set_colorkey(None, pg.RLEACCEL)

		return image
