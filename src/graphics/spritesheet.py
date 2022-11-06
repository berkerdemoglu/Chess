# Typing
from typing import Union, TYPE_CHECKING
if TYPE_CHECKING:
	from pathlib import Path

import pygame as pg


class Spritesheet:
	# TODO: convert_alpha()? and write docstrings

	def __init__(self, filename: Union[str, 'Path']):
		self.sheet = pg.image.load(filename)

	def get_image_at(self, rect: pg.Rect):
		image = pg.Surface(rect.size, pg.SRCALPHA)
		image.blit(self.sheet, (0, 0), rect)
		image.set_colorkey(None, pg.RLEACCEL)

		return image
