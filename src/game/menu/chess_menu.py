# Typing
from typing import List, Union

from graphics import Renderable

from .menu_widget import MenuWidget

# remove this later, move colors into its own module
import pygame as pg


class ChessMenu(Renderable):
	"""The menu that is visible when along with the chessboard."""
	
	def __init__(self):
		"""Initialize the widgets on the menu."""
		self.board_fen_widget = MenuWidget(10, 100, 'GET FEN', pg.Color('white'), pg.Color('black'))

		self.widgets = self._init_widget_list()

	def get_pressed_widget(self) -> Union[MenuWidget, None]:
		for widget in self.widgets:
			pass

	def _init_widget_list(self) -> List:
		"""Initialize the list that contains every widget on the menu."""
		return [getattr(self, key) for key in vars(self).keys()]

	def render(self, surface):
		for widget in self.widgets:
			widget.render(surface)
