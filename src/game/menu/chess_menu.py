# Typing
from typing import List, Union, TYPE_CHECKING
if TYPE_CHECKING:
	from chess import Board

# Imports from my packages
from graphics import Renderable
from fen_parser.board_parser import BoardParser
from .menu_widget import MenuWidget
from utils import point_in_rect

import pygame as pg  # remove this later, move colors into its own module

import tkinter.filedialog as fd
import tkinter as tk


class ChessMenu(Renderable):
	"""The menu that is visible when along with the chessboard."""
	
	def __init__(self):
		"""Initialize the widgets on the menu."""
		self.board_fen_widget = MenuWidget(
			30, 100, 'fen_widget', 'SAVE FEN', 
			pg.Color('black'), pg.Color('white'), pg.Color('black')
			)

		self.widgets = self._init_widget_list()

	def get_pressed_widget(self, mouse_x: int, mouse_y: int) -> Union[MenuWidget, None]:
		"""Return the pressed widget on the chess menu."""
		for widget in self.widgets:
			if point_in_rect(mouse_x, mouse_y, widget.rect):
				return widget

		return None  # this can be removed but explicit seems better

	def _init_widget_list(self) -> List[MenuWidget]:
		"""Initialize the list that contains every widget on the menu."""
		widgets = []
		for key in vars(self).keys():
			element = getattr(self, key)
			if type(element) == MenuWidget:
				widgets.append(element)

		return widgets

	def render(self, surface):
		for widget in self.widgets:
			widget.render(surface)


class ChessMenuHandler:
	"""Handles events that happen when a on the chess menu button is clicked."""

	def __init__(self, board_parser: BoardParser):
		"""Initialize the handler for the chess menu."""
		self.board_parser = board_parser

	def handle(self, widget: MenuWidget):
		"""Handle the pressed widget. Note: This method will never be passed 'None'"""
		if widget.id == 'fen_widget':
			# Get the FEN string for the position on the board
			board_fen = self.board_parser.parse()

			# Create tkinter window on our own so we can hide and close it
			root = tk.Tk()
			root.withdraw()

			save_file = fd.asksaveasfile(defaultextension='.fen')
			if save_file is not None:
				save_file.write(board_fen)
				save_file.close()

			# Quit tkinter
			root.destroy()
