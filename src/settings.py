"""
This module defines constants/settings for the whole application.
"""

from sys import platform

from pathlib import Path


__all__ = [
	'SRC_DIR', 
	'ROOT_DIR',
	'ASSETS_DIR'
]


# Path constants
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent

ASSETS_DIR = ROOT_DIR / 'assets'
CONFIG_DIR = ROOT_DIR / 'config'
