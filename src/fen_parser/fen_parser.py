# Type annotations
from typing import TYPE_CHECKING, NoReturn, Union
if TYPE_CHECKING:
	from pygame import Surface
	from chess import Square, Board
	from chess.piece import BasePiece

# Import it from the module to avoid a circular import
from chess.chess_constants import ChessColor

from .fen_constants import FEN_DICT
from .base_parser import BaseParser


class FENParser(BaseParser):
	"""A class that parses a FEN string and converts it into pieces."""

	def __init__(self, surface: 'Surface', fen: str, board: 'Board'):
		self.surface = surface

		self.board = board

		self.fen = fen.split(' ')
		self.ranks = self.fen[0].split('/')

	def parse(self) -> None:
		"""Parse the FEN string and set piece positions."""
		# Parse the ranks
		for i in range(len(self.ranks)):
			self._parse_rank(self.ranks[i], index=i)

		# Parse move turn
		self.board.move_turn = ChessColor.LIGHT if self.fen[1] == 'w' else ChessColor.DARK

	def _parse_rank(self, rank: str, **kwargs) -> None:
		"""Parse a rank on the chessboard."""
		index = kwargs['index']
		rank_squares = self.board.squares[index*8: (index + 1)*8]
		square_index = 0

		for ch in rank:
			if ch.isdigit():
				skip_num = int(ch)
				if 0 < skip_num <= 8:
					square_index += skip_num
				else:
					raise ValueError(f'Invalid FEN, cannot skip {skip_num} squares')
			else:
				piece = self._parse_piece(ch, rank_squares[square_index])
				self.board.pieces.append(piece)
				square_index += 1

	def _parse_piece(self, piece_letter: str, piece_square: 'Square') -> Union['BasePiece', NoReturn]:
		"""Parse a piece."""
		parsing_letter = piece_letter.lower()
		piece_color = ChessColor.LIGHT if piece_letter.isupper() else ChessColor.DARK

		try:
			piece_class = FEN_DICT[parsing_letter]
		except KeyError:
			raise ValueError(f'Invalid input: {piece_letter}')
		else:
			piece = piece_class(piece_color, piece_square, self.surface)
			piece.center_in_square(self.surface)

		return piece
