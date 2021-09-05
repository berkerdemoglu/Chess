# Type annotations
from typing import Dict, Callable

# GUI stuff
import tkinter as tk
from tkinter import messagebox
from .launcher_settings import LAUNCHER_SETTINGS as LS

from .widget_mixin import WidgetMixin
from .fen_gui import FENFrame

# Imports for starting position FEN
from chess import Board
from fen_parser import validate_fen


# Constants
LAUNCHER_FEN_KEY = 'fen'


class StartButton(tk.Button, WidgetMixin):

	def __init__(self, root: tk.Tk, command: Callable):
		super(StartButton, self).__init__(
				root, text='Start', padx=10, pady=10, command=command,
				font=LS.FONT, bg=LS.BG_COLOR, fg=LS.FG_COLOR
			)
		WidgetMixin.__init__(self, root)  # window attribute initialized

	def draw_widget(self):
		self.pack(anchor='center', padx=25, pady=25)


class LauncherWindow(tk.Tk, WidgetMixin):
	"""
	A wrapper class that handles the launcher's main window.

	Every widget inside an object of this class must be packed.
	"""

	def __init__(self, launcher_dict: Dict):
		"""Initialize the window and its properties."""
		super(LauncherWindow, self).__init__()
		self.launcher_dict = launcher_dict

		# Properties of the window
		self.title(LS.TITLE)
		self.geometry(LS.DIMENSIONS)
		self.configure(bg=LS.BG_COLOR)
		self.resizable(False, False)

		# Widgets from top to bottom
		self.heading_label = tk.Label(
				self, text='Chess', font=LS.H_FONT, fg=LS.FG_COLOR, bg=LS.BG_COLOR
			)

		self.fen_frame = FENFrame(self)

		self.start_button = StartButton(self, lambda: self.cmd_start_app())

	def draw_widget(self):
		self.heading_label.pack(anchor='center', padx=40, pady=20)

		self.fen_frame.draw_widget()
		self.start_button.draw_widget()

	# Commands
	def cmd_start_app(self):
		user_fen = self.fen_frame.get_fen()

		if validate_fen(user_fen):
			# Valid FEN, the game can start.
			self.launcher_dict[LAUNCHER_FEN_KEY] = user_fen
			self.destroy()
		else:
			# Invalid FEN, show an error to the user.
			messagebox.showerror(
					'Invalid FEN', 
					'You have entered an invalid FEN. Please enter a valid FEN and try again.'
				)


class Launcher:
	# TODO: Don't open the application if launcher GUI is closed by hand

	def __init__(self):
		"""Initialize the launcher's main window."""
		# Initialize a dict that holds info that will be used after the GUI is closed.
		self.launcher_dict = {}

		self.root = LauncherWindow(self.launcher_dict)

	def draw_widgets(self):
		"""Draw the widgets in the launcher GUI."""
		self.root.draw_widget()

	def start_launcher(self):
		"""Start the launcher."""
		self.draw_widgets()
		self.root.mainloop()

	def get(self, attribute):
		return self.launcher_dict[attribute]
