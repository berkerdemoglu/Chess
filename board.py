import pygame as pg

from typing import List

from base import BaseDrawable
from piece import BasePiece
from square import Square
from fen_reader import FENReader


class Board(BaseDrawable):
	DEFAULT_POSITION_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
	
	def __init__(self):
		"""Initialize the chessboard."""
		self.squares = None
		self.pieces: List[BasePiece] = list()

		self._create_board()

	def _create_board(self):
		"""Create the chessboard."""
		self.squares = self._setup_squares()
		self._setup_pieces()

	@staticmethod
	def _setup_squares() -> List[Square]:
		"""Create the squares on the chessboard."""
		squares = []

		for rank in range(8):
			for file in range(8):
				color = Square.LIGHT_SQUARE_COLOR if (file + rank) % 2 == 0 else Square.DARK_SQUARE_COLOR
				pos = (file * Square.SQUARE_SIZE, rank * Square.SQUARE_SIZE)

				square = Square(color, pos, file * 8 + rank)
				squares.append(square)

		return squares

	def _setup_pieces(self):
		"""Initialize the pieces on the chessboard."""
		f = FENReader(Board.DEFAULT_POSITION_FEN, self.squares, self.pieces)
		f.parse_fen()

	def get_square(self, coordinates: str):
		"""Get a square with the specified coordinates."""
		return next((square for square in self.squares if square.coordinates == coordinates), None)

	def render(self, surface):
		# Render the squares
		for square in self.squares:
			square.render(surface)

			label = Square.SQUARE_FONT.render(square.coordinates, True, Square.SQUARE_FONT_COLOR)
			surface.blit(label, square.get_pos(surface))

		# Render the pieces
		for piece in self.pieces:
			piece.render(surface)
