"""
This module defines constants/settings for the whole application.
"""

from sys import platform

from pathlib import Path
from types import SimpleNamespace


__all__ = [
	'SRC_DIR', 'ROOT_DIR',
	'ASSETS_DIR', 'PIECE_DIR',
	'SOUND_DIR'
]


# Path constants
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent

ASSETS_DIR = ROOT_DIR / 'assets'
PIECE_DIR = ASSETS_DIR / 'pieces'
SOUND_DIR = ASSETS_DIR / 'sounds'

# Launcher GUI settings for Windows
LAUNCHER_SETTINGS = SimpleNamespace(
		TITLE='Chess Launcher',  # title of the window
		DIMENSIONS="720x540",  # dimensions of the main window
		BG_COLOR="#c0c0c0",  # background color
		FG_COLOR="#323031",  # text color
		FONT=('Segoe UI', 14),  # font for normal texts
		H_FONT=('Aharoni', 22),  # font for headings
		SMALL_BUTTON_FONT=('Segoe UI', 10)  # font for small buttons
	)

# Launcher GUI settings for Mac OS
if platform == 'darwin':
	pass  # TODO: Actually write this
