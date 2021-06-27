"""
This module defines constants/settings for the whole application.
"""

from pathlib import Path

# Settings
ROOT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / 'assets'
PIECE_DIR = ASSETS_DIR / 'pieces'

# Game constants
SCREEN_PROPERTIES = (1280, 720)
WINDOW_TITLE = 'Chess'
FPS = 60
BACKGROUND_COLOR = (192, 192, 192)
