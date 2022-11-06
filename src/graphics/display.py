# Type annotations
from typing import Tuple

from abc import ABC, abstractmethod

import pygame as pg
import ctypes  # for dpi awareness

import time
from utils import time_ms


class Display(ABC):
	"""An abstract class that handles graphics."""

	def __init__(
			self, screen_properties: Tuple, title: str,
			background_color: Tuple[int, int, int]
	):
		"""Initialize pygame and the display settings."""
		# Improve resolution
		ctypes.windll.shcore.SetProcessDpiAwareness(1)

		# Init pygame
		pg.init()
		pg.font.init()

		# Init screen
		self.screen = pg.display.set_mode(screen_properties)
		pg.display.set_caption(title)

		self.WINDOW_TITLE = title
		self.BACKGROUND_COLOR = background_color

	def start(self) -> None:
		"""Start the main loop of the game."""
		while True:
			# Event handling
			self.poll_events()

			# Updates
			self.update()

			# Rendering
			self.render()
			pg.display.flip()

	@abstractmethod
	def poll_events(self) -> None:
		"""Check events regarding the window."""
		raise NotImplemented

	@abstractmethod
	def render(self) -> None:
		"""Draw/render objects to the screen."""
		self.screen.fill(self.BACKGROUND_COLOR)

	@abstractmethod
	def update(self) -> None:
		"""Update the game state."""
		raise NotImplemented
