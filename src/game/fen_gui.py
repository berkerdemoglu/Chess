# Type annotations
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
	from game import LauncherWindow

# GUI-related imports
import tkinter as tk
from .drawable import DrawableMixin
from settings import LAUNCHER_SETTINGS as LS

from chess import Board  # for default FEN


class FENEntry(tk.Entry, DrawableMixin):

	def __init__(self, frame: tk.LabelFrame):
		super(FENEntry, self).__init__(frame, width=100, borderwidth=10)
		DrawableMixin.__init__(self, frame)

		# Insert the default FEN
		self.insert(tk.END, Board.DEFAULT_POSITION_FEN)

	def draw_widget(self):
		self.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

	def get_fen(self) -> str:
		return str(self.get())

	def set_fen(self, new_fen: str = "") -> None:
		"""Set the entry text to a specified text."""
		self.insert(tk.END, new_fen)


class FENResetButton(tk.Button, DrawableMixin):
	"""
	The button that changes the FEN entry 
	widget's text to the default position FEN.
	"""

	def __init__(self, frame: tk.LabelFrame, command: Callable):
		super(FENResetButton, self).__init__(
				frame, text='Reset FEN', padx=5, pady=5, command=command,
				fg=LS.FG_COLOR, bg=LS.BG_COLOR, font=LS.SMALL_BUTTON_FONT
			)
		DrawableMixin.__init__(self, frame)  # self.window initialized

	def draw_widget(self):
		self.grid(row=1, column=0, columnspan=1, padx=5, pady=5)


class FENClearButton(tk.Button, DrawableMixin):
	"""The button that clears the user's FEN entry."""

	def __init__(self, frame: tk.LabelFrame, command: Callable):
		super(FENClearButton, self).__init__(
				frame, text='Clear Entry', padx=5, pady=5, command=command, 
				fg=LS.FG_COLOR, bg=LS.BG_COLOR, font=LS.SMALL_BUTTON_FONT
			)
		DrawableMixin.__init__(self, frame)  # self.window initialized

	def draw_widget(self):
		self.grid(row=1, column=1, columnspan=1, padx=5, pady=5)


class FENFrame(tk.LabelFrame, DrawableMixin):
	"""
	The frame that holds widgets related to FEN.

	All widgets inside an object of this class 
	must use the grid system for positioning.
	"""

	def __init__(self, root: 'LauncherWindow'):
		# Tkinter
		super(FENFrame, self).__init__(
				root, text='Starting Position FEN', padx=10, pady=10, font=LS.FONT,
				bg=LS.BG_COLOR, fg=LS.FG_COLOR
			)
		DrawableMixin.__init__(self, root)

		# Widgets
		self.fen_entry = FENEntry(self)

		self.fen_reset_button = FENResetButton(self, lambda: self.cmd_reset_fen())
		self.fen_clear_button = FENClearButton(self, lambda: self.cmd_clear_fen())

	def draw_widget(self):
		# Draw the frame first
		self.pack(anchor='center', padx=10, pady=10)

		# Draw the frame's widgets
		self.fen_entry.draw_widget()
		self.fen_reset_button.draw_widget()
		self.fen_clear_button.draw_widget()

	def get_fen(self) -> str:
		return self.fen_entry.get_fen()

	# Commands
	def cmd_reset_fen(self) -> None:
		self.fen_entry.set_fen(Board.DEFAULT_POSITION_FEN)

	def cmd_clear_fen(self) -> None:
		self.fen_entry.set_fen()  # clears it by default
