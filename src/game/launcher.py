# Type annotations
from typing import Callable

# GUI stuff
import tkinter as tk
from settings import LAUNCHER_SETTINGS as LS

from .drawable import DrawableMixin
from .fen_gui import FENFrame

from chess import Board  # for default FEN


class StartButton(tk.Button, DrawableMixin):

	def __init__(self, root: tk.Tk, command: Callable):
		super(StartButton, self).__init__(
				root, text='Start', padx=10, pady=10, command=command,
				font=LS.FONT, bg=LS.BG_COLOR, fg=LS.FG_COLOR
			)
		DrawableMixin.__init__(self, root)  # window attribute initialized

	def draw_widget(self):
		self.pack(anchor='center', padx=25, pady=25)


class LauncherWindow(tk.Tk, DrawableMixin):
	"""
	A wrapper class that handles the launcher's main window.

	Every widget inside an object of this class must be packed.
	"""

	def __init__(self):
		"""Initialize the window and its properties."""
		super(LauncherWindow, self).__init__()

		# Properties of the window
		self.title(LS.TITLE)
		self.geometry(LS.DIMENSIONS)
		self.configure(bg=LS.BG_COLOR)
		self.resizable(False, False)

		# Widgets
		self.start_button = StartButton(self, lambda: self.cmd_start)

	def draw_widget(self):
		self.start_button.draw_widget()

	# Commands
	def cmd_start(self):
		pass


class Launcher:

	def __init__(self):
		"""Initialize the launcher."""
		# Initialize a dict that holds info that will be used after the GUI is closed.
		self.launcher_dict = {
			'FEN': Board.DEFAULT_POSITION_FEN
		}

		# Initialize widgets.
		self.root = LauncherWindow()
		self.fen_frame = FENFrame(self.root, self.launcher_dict)

	def draw_widgets(self):
		"""Draw the widgets in the launcher GUI."""
		self.fen_frame.draw_widget()

		self.root.draw_widget()

	def start_launcher(self):
		"""Start the launcher."""
		self.draw_widgets()
		self.root.mainloop()
