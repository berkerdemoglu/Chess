# Type annotations
from typing import List, Tuple, Dict, Union, Type

import pygame as pg

from graphics import Renderable
from utils import point_in_rect

# Chess stuff
from .piece import BasePiece
from .square import Square
from fen_parser.fen_parser import FENParser
from .chess_constants import ChessColor
from .move import Move


class BoardCoordinate(Renderable):
	"""A class that handles drawing coordinates around the board."""
	RENDER_FONT_PROPERTIES = ('monospace', 18)
	RENDER_FONT = pg.font.SysFont(*RENDER_FONT_PROPERTIES)

	def __init__(self, coordinate: str, pos: Tuple[int, int]):
		"""Initialize the coordinate and its position on the screen."""
		self.label = BoardCoordinate.RENDER_FONT.render(coordinate, True, Square.SQUARE_FONT_COLOR)
		self.pos = pos

	def render(self, surface) -> None:
		"""Render the coordinate character."""
		surface.blit(self.label, self.pos)


class Board:
	"""Represents the chessboard."""
	DEFAULT_POSITION_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
	
	def __init__(self, surface: pg.Surface, fen_str: str):
		"""Initialize the chessboard."""
		self.surface = surface
		self.board_coordinates: List[BoardCoordinate]  # visual coordinates around the board

		self.squares: List[Square] = []
		self.pieces: List[BasePiece] = []
		self.piece_dict: Dict[Square: BasePiece] = {}
		self.move_turn: ChessColor
		self._move_number: int = 0

		# Declare the king variables here, these will be defined in the FEN parser
		self.white_king: King
		self.black_king: King

		# Set up the chessboard
		self._create_board(fen_str)

	def get_fullmove_number(self):
		"""Returns the full move number of the current game."""
		return (self._move_number + 2) // 2

	def increment_move_number(self, increment=1):
		"""Increments the number of half moves made."""
		self._move_number += increment

	def _create_board(self, fen_str: str):
		"""Create the chessboard with squares, pieces and coordinates around the board."""
		# Squares
		self._setup_squares()

		# Pieces
		self._setup_pieces(fen_str)
		self.update_piece_dict()

		# Coordinates around the board (for graphics/GUI)
		self.board_coordinates = self._setup_coordinates()

	def update_piece_dict(self) -> None:
		self.piece_dict.clear()

		for piece in self.pieces:
			self.piece_dict[piece.square] = piece

	def _setup_squares(self) -> None:
		"""Initialize the squares on the chessboard."""
		for rank in range(8):
			for file in range(8):
				color = ChessColor.LIGHT if (file + rank) % 2 == 0 else ChessColor.DARK
				pos = (file * Square.SQUARE_SIZE, rank * Square.SQUARE_SIZE)
				index = rank*8 + file

				square = Square(color, pos, index, self.surface)
				self.squares.append(square)

	def _setup_pieces(self, fen_str: str) -> None:
		"""Initialize the pieces on the chessboard."""
		fen_parser = FENParser(self.surface, fen_str, self)
		fen_parser.parse()

	def _setup_coordinates(self) -> List[BoardCoordinate]:
		"""Initialize the coordinate strings around the chessboard."""
		coordinates = []

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

	# TODO: Use binary search since the data is sorted or use dictionaries
	# Getters
	def get_square_by_coords(self, x: int, y: int) -> Union[Square, None]:
		"""Get a square from the board with the specified x, y coordinates."""
		for square in self.squares:
			if point_in_rect(x, y, square.rect):
				return square

		return None  # not required, but it does make it explicit

	def get_piece_by_coords(self, x: int, y: int) -> Union[BasePiece, None]:
		"""Get a piece from the board with the specified coordinates."""
		for piece in self.pieces:
			if point_in_rect(x, y, piece.rect):
				return piece

		return None  # not required, but it does make it explicit

	def get_piece_occupying_square(self, square: Square) -> Union[BasePiece, None]:
		"""Get a piece from the board occupying the specified square."""
		return self.piece_dict.get(square, None)

	def get_pieces(self, piece_type: Type[BasePiece], piece_color: ChessColor) -> List[BasePiece]:
		"""Get pieces that fit the given description, as in type and color."""
		pieces_to_return = []

		for piece in self.pieces:
			if piece.__class__ == piece_type and piece.color == piece_color:
				pieces_to_return.append(piece)

		return pieces_to_return

	def render(self, dragged_piece: BasePiece):
		"""Render the chessboard."""
		# Render the squares.
		for square in self.squares:
			square.render(self.surface)

		# Render the coordinates.
		for coord in self.board_coordinates:
			coord.render(self.surface)

		# Render the pieces.
		for piece in self.pieces:
			if piece != dragged_piece:
				piece.render(self.surface)

		# Render the piece being dragged last so that its on top of the other pieces.
		if dragged_piece is not None:
			dragged_piece.render(self.surface)
