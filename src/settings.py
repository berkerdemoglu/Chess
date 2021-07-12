"""
This module defines constants/settings for the whole application.
"""

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

# Launcher GUI settings ('L_' stands for 'Launcher')
LAUNCHER_SETTINGS = SimpleNamespace(
		TITLE='Chess Launcher',
		DIMENSIONS="720x540",
		BG_COLOR="#c0c0c0"
	)
