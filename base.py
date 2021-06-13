from abc import ABC, abstractmethod

from typing import Dict


class BaseDrawable(ABC):

	def _parse_kwargs(self, kwargs) -> None:
		"""
		Parse and set attributes if they are in the possible keyword arguments list.
		"""
		try:
			possible_kwargs = self.__class__.possible_kwargs
		except AttributeError:
			raise AttributeError(f'This class does not have possible_kwargs defined')
		else:
			for k, v in kwargs.items():
				if k in possible_kwargs:
					setattr(self, k, v)

	@abstractmethod
	def render(self, surface) -> None:
		raise NotImplemented
