# Typing
from typing import Tuple

import pygame as pg

from graphics import Renderable


class MenuWidget(Renderable):
	MENU_FONT = pg.font.SysFont('monospace', 18)
	WIDGET_HEIGHT = 30
	WIDGET_WIDTH = 100

	def __init__(
			self, x:int, y:int, text:str, 
			text_color: Tuple[int, int, int], 
			bg_color: Tuple[int, int, int]
		):
		self.x = x
		self.y = y
		self.pos = (self.x, self.y)

		self.text = text
		self.text_color = text_color
		self.bg_color = bg_color

		# Graphics
		self.rect = self._init_rect()
		self.label = MenuWidget.MENU_FONT.render(text, True, self.text_color)

	def render(self, surface):
		pg.draw.rect(surface, self.bg_color, self.rect)  # background
		surface.blit(self.label, self.pos)  # text

	def _init_rect(self) -> None:
		return pg.Rect(
				self.x, self.y, MenuWidget.WIDGET_WIDTH, MenuWidget.WIDGET_HEIGHT
			)
