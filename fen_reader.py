from typing import List

from square import Square
from constants import PieceColor
from piece import BasePiece, Pawn, Knight, Bishop, Rook, Queen, King


class FENReader:

	def __init__(self, fen: str, squares: List[Square], pieces_list: List):
		self.squares = squares
		self.pieces = pieces_list

		self.fen = fen.split(' ')[0]
		self.ranks = self.fen.split('/')

	def parse_fen(self) -> None:
		"""Parse the FEN string and set piece positions."""
		for i in range(len(self.ranks)):
			self.parse_rank(self.ranks[i], i)

		print(self.pieces)

	def parse_rank(self, rank: str, index: int) -> None:
		"""Parse a rank on the chessboard."""
		rank_squares = self.squares[index*8: (index + 1)*8]
		square_index = 0

		for i in range(len(rank)):
			ch = rank[i]
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

	@staticmethod
	def parse_piece(piece_letter: str, piece_square: Square) -> BasePiece:
		"""Parse a piece."""
		parsing_letter = piece_letter.lower()
		piece_color = PieceColor.LIGHT if piece_letter.isupper() else PieceColor.DARK
		piece = None

		if parsing_letter == 'p':
			piece = Pawn(piece_color, piece_square)
		elif parsing_letter == 'b':
			piece = Bishop(piece_color, piece_square)
		elif parsing_letter == 'n':
			piece = Knight(piece_color, piece_square)
		elif parsing_letter == 'r':
			piece = Rook(piece_color, piece_square)
		elif parsing_letter == 'q':
			piece = Queen(piece_color, piece_square)
		elif parsing_letter == 'k':
			piece = King(piece_color, piece_square)
		else:
			raise ValueError(f'Invalid input: {piece_letter}')

		return piece
