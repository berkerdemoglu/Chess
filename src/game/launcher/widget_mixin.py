from abc import ABC, abstractmethod


class WidgetMixin(ABC):
	"""An abstract base class for widgets."""

	def __init__(self, window):
		"""Initialize the widget's window attribute."""
		self.window = window

	@abstractmethod
	def draw_widget(self) -> None:
		"""Draw the widget on the screen."""
		raise NotImplemented
