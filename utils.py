from pygame import Rect


def point_in_rect(x: int, y: int, rect: Rect) -> bool:
	"""Check if a point is in a rect."""
	rect_x1, rect_y1, width, height = rect
	rect_x2 = rect_x1 + width
	rect_y2 = rect_y1 + height

	if rect_x1 <= x <= rect_x2 and rect_y1 <= y <= rect_y2:
		return True

	return False
