import os
import sys
import json
import logging
import traceback

# Global Variables
DEFAULT_STATUS_CODE = [200]

def handle_error(msg, err=None):
	""" Serves as Generic Error handling Function """

	# Log the error msg and exit
	logging.critical(msg)

	# Check if any exception present
	if err is not None:		
		logging.critical('Exception : '.format(err))
		logging.critical("Additional Info : {}".format(traceback.format_exc()))
	logging.critical('Exiting Program...')
	exit(1)

