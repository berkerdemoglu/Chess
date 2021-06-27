from chess import piece


FEN_DICT = {
	'p': piece.Pawn, 'n': piece.Knight, 'b': piece.Bishop,
	'r': piece.Rook, 'q': piece.Queen, 'k': piece.King
}


BOARD_DICT = {v: k for k, v in FEN_DICT.items()}
