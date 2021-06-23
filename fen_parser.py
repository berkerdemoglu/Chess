from typing import List

from square import Square
from constants import SquareColor
from piece import BasePiece, Pawn, Knight, Bishop, Rook, Queen, King


class FENParser:
	FEN_DICT = {
		'p': Pawn, 'n': Knight, 'b': Bishop,
		'r': Rook, 'q': Queen, 'k': King
	}

	def __init__(self, surface, fen: str, squares: List[Square], pieces_list: List):
		self.surface = surface   # pygame.Surface

		self.squares = squares
		self.pieces = pieces_list

		self.fen = fen.split(' ')[0]
		self.ranks = self.fen.split('/')

	def parse_fen(self) -> None:
		"""Parse the FEN string and set piece positions."""
		for i in range(len(self.ranks)):
			self.parse_rank(self.ranks[i], i)

	def parse_rank(self, rank: str, index: int) -> None:
		"""Parse a rank on the chessboard."""
		rank_squares = self.squares[index*8: (index + 1)*8]
		square_index = 0

		for ch in rank:
			if ch.isdigit():
				skip_num = int(ch)
				if 0 < skip_num <= 8:
					square_index += skip_num
				else:
					raise ValueError(f'Invalid fen, cannot skip {skip_num} squares')
			else:
				piece = self.parse_piece(ch, rank_squares[square_index])
				self.pieces.append(piece)
				square_index += 1

	def parse_piece(self, piece_letter: str, piece_square: Square) -> BasePiece:
		"""Parse a piece."""
		parsing_letter = piece_letter.lower()
		piece_color = SquareColor.LIGHT if piece_letter.isupper() else SquareColor.DARK

		piece_class = FENParser.FEN_DICT[parsing_letter]
		try:
			piece = piece_class(piece_color, piece_square)
			piece.center_in_square(self.surface)
		except KeyError:
			raise ValueError(f'Invalid input: {piece_letter}')

		return piece
