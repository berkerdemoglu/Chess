# Type annotations
from typing import Dict, Union, TYPE_CHECKING
if TYPE_CHECKING:
	from pathlib import Path

from collections import namedtuple


# Define what can be imported from this module
__all__ = ['IniParser', 'ConfigError']


# A class for a configuration
_Configuration = namedtuple('_ConfigSettings', 'setting_name, setting_value')


class ConfigError(Exception):
	"""
	An exception that is raised when there's 
	an error with reading the configuration file.
	"""
	# TODO: Make the error message more informative

	def __init__(self, config_filename):
		super().__init__(f'An error occured while parsing file {config_filename}.')


class IniParser:
	"""Parses an initialization/configuration file."""

	def __init__(self, filename: Union[str, 'Path']):
		"""Initialize the reader with a filename to read."""
		self.filename = filename

	def read_config(self) -> Dict:
		"""Read the file and return variables in a dictionary."""
		settings = {}

		with open(self.filename, 'r') as f:
			lines = f.readlines()

		for line in lines:
			if line == '\n' or line.startswith('//'):
				# Skip the line if it's empty or a comment.
				continue

			setting = self._parse_config(line)

			settings[setting.setting_name] = setting.setting_value

		return settings

	def _parse_config(self, line: str) -> _Configuration:
		"""Parse a configuration from the file."""
		if line.count('=') != 1:
			# Make sure that there is just one equal sign
			raise ConfigError(self.filename)

		variable_data = line.split('=')
		varname = variable_data[0].strip()
		value = variable_data[1].strip()

		# Convert value to float or int if possible
		try:
			value = int(value)
		except ValueError:
			try:
				value = float(value)
			except ValueError:
				pass

		setting = _Configuration(varname, value)
		return setting
