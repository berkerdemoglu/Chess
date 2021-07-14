# Type annotations
from typing import Dict, Callable

from abc import ABC, abstractmethod

# GUI stuff
import tkinter as tk
from settings import LAUNCHER_SETTINGS as LS

from chess import Board


class DrawableMixin(ABC):  # TODO: rename to 'WidgetMixin'
	"""An abstract base class for widgets."""

	def __init__(self, window):
		"""Initialize the widget's window attribute."""
		self.window = window

	@abstractmethod
	def draw_widget(self) -> None:
		"""Draw the widget on the screen."""
		raise NotImplemented


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


class FENEntry(tk.Entry, DrawableMixin):

	def __init__(self, frame: tk.LabelFrame):
		super(FENEntry, self).__init__(frame, width=100, borderwidth=10)
		DrawableMixin.__init__(self, frame)

		# Insert default FEN
		self.insert(tk.END, Board.DEFAULT_POSITION_FEN)

	def draw_widget(self):
		self.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

	def set_fen(self, launcher_dict: Dict) -> str:
		launcher_dict['FEN'] = str(self.get())


class FENResetButton(tk.Button, DrawableMixin):

	def __init__(self, frame: tk.LabelFrame, command: Callable):
		super(FENButton, self).__init__(frame)
		DrawableMixin.__init__(self, frame)  # self.window initialized

	def draw_widget(self):
		pass


class FENFrame(tk.LabelFrame, DrawableMixin):
	"""The frame that holds widgets related to FEN."""

	def __init__(self, root: LauncherWindow, launcher_dict: Dict):
		# Tkinter
		super(FENFrame, self).__init__(
				root, text='Starting Position FEN', padx=10, pady=10, font=LS.FONT,
				bg=LS.BG_COLOR, fg=LS.FG_COLOR
			)
		DrawableMixin.__init__(self, root)

		# Keep a reference of the launcher dictionary here.
		self.launcher_dict = launcher_dict

		# Widgets
		self.fen_entry = FENEntry(self)

	def draw_widget(self):
		# Draw the frame first
		self.pack(anchor='center', padx=10, pady=10)

		# Draw the frame's widgets
		# Important: All widgets inside FENFrame must use gridding
		self.fen_entry.draw_widget()


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
