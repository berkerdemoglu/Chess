# Type annotations
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
	from chess import Board, Square

from .base_parser import BaseParser
from chess import ChessColor
from .fen_constants import BOARD_DICT


class BoardParser(BaseParser):

	def __init__(self, board: 'Board'):
		self.board = board
		self.fen_str = ""

	def parse(self) -> str:
		# Parse ranks
		for i in range(8):
			rank = self.board.squares[i*8: (i+1)*8]
			self._parse_rank(rank)

		# Remove the last slash '/'
		self.fen_str = self.fen_str[:-1]

		# Add move turn to the FEN
		self.fen_str += ' w' if self.board.move_turn == ChessColor.LIGHT else ' b'

		# Reset the FEN string
		return_str = self.fen_str
		self.fen_str = ""
		return return_str

	def _parse_rank(self, rank: List['Square']) -> None:
		rank_str = ""
		skipped = 0

		for square in rank:
			# Get piece on that square
			piece = self.board.get_piece_occupying_square(square)

			if piece is not None:
				piece_str = BOARD_DICT[type(piece)]
				piece_str = piece_str.upper() if piece.color == ChessColor.LIGHT else piece_str

				if skipped >= 1:  # we skipped squares
					rank_str += str(skipped) + piece_str
				else:  # we didn't skip any squares
					rank_str += piece_str

				skipped = 0
			else:
				skipped += 1

		if skipped != 0:
			rank_str += str(skipped)

		rank_str += "/"

		self.fen_str += rank_str
