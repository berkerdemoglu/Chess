from abc import ABC, abstractmethod


class BaseDrawable(ABC):

	@abstractmethod
	def render(self, surface) -> None:
		raise NotImplemented
