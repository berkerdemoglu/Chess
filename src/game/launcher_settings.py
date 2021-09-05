from types import SimpleNamespace

from settings import CONFIG_DIR
from ini_parser import IniParser, ConfigError


config_filename = CONFIG_DIR / 'launcher.ini'
ini_parser = IniParser(CONFIG_DIR / 'launcher.ini')
config = ini_parser.read_config()


try:
	LAUNCHER_SETTINGS = SimpleNamespace(
		# Title of the window
		TITLE=config['LNCH_TITLE'],

		# Dimensions of the main window
		DIMENSIONS=f"{config['LNCH_DIMENSION_X']}x{config['LNCH_DIMENSION_Y']}",
		
		# Background color
		BG_COLOR=config['LNCH_BG_COLOR'],
		
		# Text color
		FG_COLOR=config['LNCH_FG_COLOR'],
		
		# Font for normal texts
		FONT=(config['LNCH_FONT_NAME'], config['LNCH_FONT_SIZE']),
		
		# Font for headings
		H_FONT=(config['LNCH_H_FONT_NAME'], config['LNCH_H_FONT_SIZE']),
		
		# Font for small buttons
		SMALL_BUTTON_FONT=(config['LNCH_SMALL_BUTTON_FONT_NAME'], config['LNCH_SMALL_BUTTON_FONT_SIZE'])
	)
except KeyError:
	raise ConfigError(config_filename)
