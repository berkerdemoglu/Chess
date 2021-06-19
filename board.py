import pygame as pg

from typing import List, Tuple

from base import BaseDrawable
from utils import point_in_rect
from piece import BasePiece
from square import Square
from fen_parser import FENParser
from constants import SQUARE_FONT_COLOR, PieceColor


class BoardCoordinate(BaseDrawable):
	"""A class that handles drawing coordinates around the board."""
	RENDER_FONT_PROPERTIES = ('monospace', 18)
	RENDER_FONT = pg.font.SysFont(*RENDER_FONT_PROPERTIES)

	def __init__(self, coordinate: str, pos: Tuple[int, int]):
		"""Initialize the coordinate and its position on the screen."""
		self.label = BoardCoordinate.RENDER_FONT.render(coordinate, True, SQUARE_FONT_COLOR)
		self.pos = pos

	def render(self, surface) -> None:
		"""Render the coordinate character."""
		surface.blit(self.label, self.pos)


class Board:
	"""Represents the chessboard."""
	DEFAULT_POSITION_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
	
	def __init__(self, surface: pg.Surface):
		"""Initialize the chessboard."""
		self.surface = surface
		self.board_coordinates: List[BoardCoordinate]  # visual coordinates around the board

		self.squares: List[Square]
		self.pieces: List[BasePiece] = list()
		self.move_turn: PieceColor = PieceColor.LIGHT

		self._create_board()

	def _create_board(self):
		"""Create the chessboard with squares, pieces and coordinates around the board."""
		self.squares = self._setup_squares()
		self._setup_pieces()
		self.board_coordinates = self._setup_coordinates()

	@staticmethod
	def _setup_squares() -> List[Square]:
		"""Initialize the squares on the chessboard."""
		squares = list()

		for rank in range(8):
			for file in range(8):
				color = Square.LIGHT_SQUARE_COLOR if (file + rank) % 2 == 0 else Square.DARK_SQUARE_COLOR
				pos = (file * Square.SQUARE_SIZE, rank * Square.SQUARE_SIZE)

				square = Square(color, pos, file*8 + rank)
				squares.append(square)

		return squares

	def _setup_pieces(self) -> None:
		"""Initialize the pieces on the chessboard."""
		f = FENParser(self.surface, Board.DEFAULT_POSITION_FEN, self.squares, self.pieces)
		f.parse_fen()

	def _setup_coordinates(self) -> List[BoardCoordinate]:
		"""Initialize the coordinate strings around the chessboard."""
		coordinates = list()

		# a, b, c, d, e, f, g, h - horizontal, files
		for i in range(56, 64):
			square = self.squares[i]
			pos = square.get_pos(self.surface)
			x = pos[0] + Square.SQUARE_SIZE / 2.5
			y = pos[1] + Square.SQUARE_SIZE*1.1

			coordinate = BoardCoordinate(square.coordinates[0], (x, y))
			coordinates.append(coordinate)

		# 1, 2, 3, 4, 5, 6, 7, 8 - vertical, ranks
		for i in range(7, 64, 8):
			square = self.squares[i]
			pos = square.get_pos(self.surface)
			x = pos[0] + Square.SQUARE_SIZE*1.1
			y = pos[1] + Square.SQUARE_SIZE / 2.5

			coordinate = BoardCoordinate(square.coordinates[1], (x, y))
			coordinates.append(coordinate)

		return coordinates

	# Getters
	def get_square_by_coords(self, x: int, y: int):
		"""Get a square from the board with the specified coordinates."""
		for square in self.squares:
			if point_in_rect(x, y, square.get_rect(self.surface)):
				return square

	def get_piece_by_coords(self, x: int, y: int) -> BasePiece:
		"""Get a piece from the board with the specified coordinates."""
		for piece in self.pieces:
			if point_in_rect(x, y, piece.rect):
				return piece

	def get_piece_occupying_square(self, square: Square) -> BasePiece:
		"""Get a piece from the board occupying the specified square."""
		for piece in self.pieces:
			if piece.square == square:
				return piece

	def render(self, dragged_piece: BasePiece):
		"""Render the chessboard."""
		# Render the squares
		for square in self.squares:
			square.render(self.surface)

		# Render the coordinates
		for coord in self.board_coordinates:
			coord.render(self.surface)

		# Render the pieces
		for piece in self.pieces:
			if piece != dragged_piece:
				piece.render(self.surface)
		# Render the piece being dragged last so that its on top of the other pieces
		if dragged_piece is not None:
			dragged_piece.render(self.surface)
