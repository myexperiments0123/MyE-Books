import json
import logging 
from custom_library import handle_error

def read_config():
	""" Reads the Config Details from CONFIG_FILE and converts to JSON Object"""
	CONFIG_FILE = 'config.json'

	#Open CONFIG_FILE and loads JSON data 
	with open(CONFIG_FILE) as fd:
		try:
			# Convert File data to JSON
			return json.load(fd)			

		# Catch the throwed exception
		except Exception as err:
			handle_error('An error occured while converting "{}" to JSON:'.format(CONFIG_FILE)
						, err)

class Config(object):
	"""Class to parse Configuration Settings"""
	for key, value in read_config().items():
		locals()[key] = value

