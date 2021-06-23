from typing import Tuple
from abc import ABC, abstractmethod

import pygame as pg

import time
from utils import time_ms


class BaseRenderable(ABC):
	"""An abstract class for objects that can be rendered to the screen."""

	@abstractmethod
	def render(self, surface: pg.Surface) -> None:
		"""Render the object to the screen."""
		raise NotImplemented


class BaseDisplay(ABC):
	"""An abstract class that handles graphics."""

	def __init__(
			self, screen_properties: Tuple, title: str,
			fps: int, background_color: Tuple[int, int, int]
	):
		"""Initialize the display."""
		pg.init()
		self.screen = pg.display.set_mode(screen_properties)
		pg.display.set_caption(title)

		self.WINDOW_TITLE = title
		self.FPS = fps
		self.BACKGROUND_COLOR = background_color

	def start(self) -> None:
		"""Start the main loop of the game."""
		update_frequency = 1000000000 / self.FPS
		delta = 0
		drawn_frames = 0

		now_nano: int
		last_nano = time.time_ns()
		second_counter = time_ms()

		while True:
			now_nano = time.time_ns()
			delta += (now_nano - last_nano) / update_frequency
			last_nano = now_nano

			while delta >= 1:
				# Event handling
				self.poll_events()

				# Updates
				self.update()
				delta -= 1

				# Rendering
				self.render()
				pg.display.flip()  # actually make the scene visible
				drawn_frames += 1

			if time_ms() - second_counter > 1000:
				second_counter += 1000
				pg.display.set_caption(f'{self.WINDOW_TITLE} - {drawn_frames}fps')
				drawn_frames = 0

	@abstractmethod
	def poll_events(self) -> None:
		"""Check events regarding the window."""
		raise NotImplemented

	@abstractmethod
	def render(self) -> None:
		"""
		Draw/render objects to the screen.
		By default, this method fills the screen with the background color.
		"""
		self.screen.fill(self.BACKGROUND_COLOR)

	@abstractmethod
	def update(self) -> None:
		"""Update the game state."""
		raise NotImplemented
