# Type annotations
from typing import TYPE_CHECKING, NoReturn, Union
if TYPE_CHECKING:
	from pygame import Surface
	from chess import Square, Board

# Import it from the module to avoid a circular import
from chess.chess_constants import ChessColor
from chess.piece import BasePiece, King

from .fen_constants import FEN_DICT
from .base_parser import BaseParser


class FENParser(BaseParser):
	"""A class that parses a FEN string and converts it into pieces."""
	# TODO: If king is not on e4, then has_moved = True

	def __init__(self, surface: 'Surface', fen: str, board: 'Board'):
		self.surface = surface

		self.board = board

		self.fen = fen.split(' ')
		self.ranks = self.fen[0].split('/')
		self.castling_rights = self.fen[2]

	def parse(self) -> None:
		"""Parse the FEN string and set piece positions."""
		# Parse the ranks
		for i in range(len(self.ranks)):
			self._parse_rank(self.ranks[i], index=i)

		# Parse move turn
		self.board.move_turn = ChessColor.LIGHT if self.fen[1] == 'w' else ChessColor.DARK

	def _parse_castling_rights(
			self, white_king: King, black_king: King
		):
		pass

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

	def _set_king_has_moved(self, king: 'King'):
		if king.color == ChessColor.LIGHT:
			# White king
			if king.square.coordinates != 'e4':
				# Must be on e4 to castle
				king.has_moved = True
			else:
				king.has_moved = False
		else:
			# Black king
			if king.square.coordinates != 'e8':
				# Must be on e8 to castle
				king.has_moved = True
			else:
				king.has_moved = False
