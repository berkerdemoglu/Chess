# Type annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from pygame import Surface

from abc import abstractmethod, ABC


class Renderable(ABC):
	"""An abstract class for objects that can be rendered to the screen."""

	@abstractmethod
	def render(self, surface: 'Surface') -> None:
		"""Render the object to the screen."""
		raise NotImplemented
