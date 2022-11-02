# Typing
from typing import Tuple

import pygame as pg

from graphics import Renderable


class MenuWidget(Renderable):
	"""Represents a widget on the in-game menu."""
	# TODO: Add some good styling to the widget
	MENU_FONT = pg.font.SysFont('monaco', 18)
	WIDGET_HEIGHT = 60
	WIDGET_WIDTH = 150

	def __init__(
			self, x:int, y:int, identifier: str, text:str, 
			text_color: Tuple[int, int, int], 
			bg_color: Tuple[int, int, int]
		):
		"""Initialize the widget and the text inside it."""
		self.x = x
		self.y = y
		self.id = identifier

		self.text = text
		self.text_color = text_color
		self.bg_color = bg_color

		# Graphics
		self.rect = self._init_rect()
		self.label = MenuWidget.MENU_FONT.render(text, True, self.text_color)
		self.label_pos = self._center_label_pos()

	def _center_label_pos(self) -> Tuple[int, int]:
		"""Centers the label inside the widget."""
		center_x = (MenuWidget.WIDGET_WIDTH // 2) + self.x - (self.label.get_width() // 2)
		center_y = (MenuWidget.WIDGET_HEIGHT // 2) + self.y - (self.label.get_height() // 2)

		return center_x, center_y

	def render(self, surface):
		pg.draw.rect(surface, self.bg_color, self.rect)  # background
		surface.blit(self.label, self.label_pos)  # text

	def _init_rect(self) -> None:
		return pg.Rect(
				self.x, self.y, MenuWidget.WIDGET_WIDTH, MenuWidget.WIDGET_HEIGHT
			)
