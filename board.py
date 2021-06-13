from base import BaseDrawable
from constants import WHITE, BLACK
from square import Square


class Board(BaseDrawable):

	def __init__(self):
		self.squares = Board._create_board()

	@classmethod
	def _create_board(cls):
		squares = []

		for file in range(8):
			for rank in range(8):
				color = WHITE if (file+rank) % 2 == 0 else BLACK
				pos = (file * Square.SQUARE_SIZE, rank * Square.SQUARE_SIZE)
				square = Square(color, pos)
				print(f'Square - {square}')
				squares.append(square)

		return squares

	def render(self, surface):
		for square in self.squares:
			square.render(surface)
