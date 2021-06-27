"""
This module defines constants/settings for the whole application.
"""

from pathlib import Path

# Path constants
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent

ASSETS_DIR = ROOT_DIR / 'assets'
PIECE_DIR = ASSETS_DIR / 'pieces'
