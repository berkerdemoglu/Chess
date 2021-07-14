import re


VALIDATOR_REGEX = re.compile(
	r'\s*([rnbqkpRNBQKP1-8]+\/){7}([rnbqkpRNBQKP1-8]+)' +
	r'\s[bw-]\s(([a-hkqA-HKQ]{1,4})|(-))\s(([a-h][36])|(-))\s\d+\s\d+\s*'
)


def validate_fen(fen: str) -> bool:
	"""Check the validity of a given FEN string."""
	match_obj = re.match(VALIDATOR_REGEX, fen)

	if match_obj is None:
		return False

	return True
