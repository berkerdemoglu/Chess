# Type annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from chess import Board

from abc import ABC, abstractmethod


class BaseParser(ABC):

	def __init(self, board: 'Board'):
		self.board = board

	@abstractmethod
	def parse(self, *args, **kwargs):
		raise NotImplemented

	@abstractmethod
	def _parse_rank(self, rank, *args, **kwargs):
		raise NotImplemented
