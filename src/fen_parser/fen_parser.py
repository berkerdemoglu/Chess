# Type annotations
from typing import TYPE_CHECKING, NoReturn, Union
if TYPE_CHECKING:
	from pygame import Surface
	from chess import Square, Board

from utils import sort_word_by_case

# Import it from the module to avoid a circular import
from chess.chess_constants import ChessColor
from chess.piece import BasePiece, King

from .fen_constants import FEN_DICT
from .base_parser import BaseParser


class FENParser(BaseParser):
	"""A class that parses a FEN string and converts it into pieces."""

	def __init__(self, surface: 'Surface', fen: str, board: 'Board'):
		self.surface = surface

		self.board = board

		self.fen = fen.split(' ')
		self.ranks = self.fen[0].split('/')
		self.castling_rights = self.fen[2]

	def parse(self) -> None:
		"""Parse the FEN string and set piece positions."""
		# TODO: Make the user enter another FEN if there is an error parsing it
		# Parse the ranks
		for i in range(len(self.ranks)):
			self._parse_rank(self.ranks[i], i)

		# Parse move turn
		self.board.move_turn = ChessColor.LIGHT if self.fen[1] == 'w' else ChessColor.DARK

		# Parse castling rights
		self.board.white_king = self._get_king(ChessColor.LIGHT)
		self.board.black_king = self._get_king(ChessColor.DARK)
		self._parse_castling_rights()

	def _parse_castling_rights(self):
		# TODO: Note to self, what do you do if there is no rook to castle with?
		# TODO: What do you do if there is no king on the board?
		white_rights, black_rights = sort_word_by_case(self.castling_rights)

		self.board.white_king.init_fen_castling_rights(white_rights)
		self.board.black_king.init_fen_castling_rights(black_rights)

	def _get_king(self, color: ChessColor):
		return self.board.get_pieces(King, color)[0]

	def _parse_rank(self, rank: str, index: int) -> None:
		"""Parse a rank on the chessboard."""
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
		# TODO: Implement this after the castling rights thing
		if king.color == ChessColor.LIGHT:
			# White king
			if king.square.coordinates != 'e1':
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
