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

		# Insert default FEN
		self.insert(tk.END, Board.DEFAULT_POSITION_FEN)

	def draw_widget(self):
		self.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

	def get_fen(self) -> str:
		return str(self.get())


class FENResetButton(tk.Button, DrawableMixin):

	def __init__(self, frame: tk.LabelFrame, command: Callable):
		super(FENButton, self).__init__(frame)
		DrawableMixin.__init__(self, frame)  # self.window initialized

	def draw_widget(self):
		pass


class FENFrame(tk.LabelFrame, DrawableMixin):
	"""The frame that holds widgets related to FEN."""

	def __init__(self, root: 'LauncherWindow'):
		# Tkinter
		super(FENFrame, self).__init__(
				root, text='Starting Position FEN', padx=10, pady=10, font=LS.FONT,
				bg=LS.BG_COLOR, fg=LS.FG_COLOR
			)
		DrawableMixin.__init__(self, root)

		# Widgets
		self.fen_entry = FENEntry(self)

	def draw_widget(self):
		# Draw the frame first
		self.pack(anchor='center', padx=10, pady=10)

		# Draw the frame's widgets
		# Important: All widgets inside FENFrame must use gridding
		self.fen_entry.draw_widget()

	def get_fen(self):
		return self.fen_entry.get_fen()
