from abc import ABC, abstractmethod

import tkinter as tk
from settings import LAUNCHER_SETTINGS as LS

from chess import Board


class DrawableMixin(ABC):
	"""An abstract base class for widgets."""

	@abstractmethod
	def draw_widget(self) -> None:
		"""Draw the widget on the screen."""
		raise NotImplemented


class LauncherWindow(tk.Tk):
	"""A wrapper class that handles the launcher's main window."""

	def __init__(self):
		"""Initialize the window and its properties."""
		super().__init__()

		self.title(LS.TITLE)
		self.geometry(LS.DIMENSIONS)
		self.configure(bg=LS.BG_COLOR)
		self.resizable(False, False)


class FENEntry(tk.Entry, DrawableMixin):

	def __init__(self, root: tk.Tk):
		super(FENEntry, self).__init__(root, width=100, borderwidth=5)

		# Insert default FEN
		self.insert(tk.END, Board.DEFAULT_POSITION_FEN)

	def draw_widget(self):
		self.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

	def get_fen(self) -> str:
		return str(self.get())


class FENFrame(tk.LabelFrame):

	def __init__(self, root: tk.Tk):
		pass


class Launcher:

	def __init__(self):
		"""Initialize the launcher."""
		self.root = LauncherWindow()
		self.fen_entry = FENEntry(self.root)

	def draw_widgets(self):
		"""Draw the widgets in the GUI."""
		self.fen_entry.draw_widget()

	def start_launcher(self):
		"""Start the launcher."""
		self.draw_widgets()
		self.root.mainloop()
