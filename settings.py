"""
This module defines constants/settings for the whole application.
"""

from pathlib import Path

# Settings
ROOT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / 'assets'
PIECE_DIR = ASSETS_DIR / 'pieces'
