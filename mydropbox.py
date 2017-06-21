import os
import sys
import json
import logging
import requests
from pprint import pprint
from custom_library import handle_error
from config_parser import Config

class MyDropbox(object):
	""" Custom class for Custom Dropbox Operation"""
	
	# Create Static Variables from CONFIG
	EXISTING_FILES = []

	for key, value in Config.DROPBOX.items():
		locals()[key] = value

	@staticmethod
	def get_dropbox_usage():
		""" Get the usage of the dropbox """

		# Call API Request to get the current usage of dropbox
		current_usage = MyDropbox.http_post(MyDropbox.API_USAGE, data=json.dumps(None))['used']
		return current_usage		
		
	@staticmethod
	def get_all_available_files():
		""" Retrive all Available files in given folder of Dropbox """
		
		# Set Folder location in HTML DATA
		data = {
    		"path": MyDropbox.FOLDER_LOCATION,
    	}

    	# Call LIST FOLDER API request
		response = MyDropbox.http_post(MyDropbox.API_LISTFOLDER, data=json.dumps(data))

		# Add the existing files to list
		MyDropbox.EXISTING_FILES = [entry['name'] for entry in response['entries']]

		# Iterate over all the pages using cursor
		while response['has_more']:
			# Set the cursor to get next response
			data = {
				"cursor" : response['cursor']
			}	
			# Call API request		
			response = MyDropbox.http_post(MyDropbox.API_LISTFOLDER_CONTINUE, data=json.dumps(data))
			# Add the existing files to list
			MyDropbox.EXISTING_FILES += [entry['name'] for entry in response['entries']]

	@staticmethod
	def upload_file(file):
		""" Validate and Upload the file """

		# Validate the file
		if not os.path.isfile(file):
			handle_error('File Not Found : {}'.format(file))

		# Set folder location in Headers
		extra_headers = {		    
		    "Dropbox-API-Arg": '{"path":"/ebooks/{}","autorename":false,"mute":false,"mode":{".tag":"add"}}'.format(file)
		}

		# read the file content in binary format
		with open(file, "rb") as fd:
			data = fd.read()

		# Call api request to uplad the file
		MyDropbox.http_post(MyDropbox.API_UPLOAD, extra_headers=extra_headers, data=data)
		return True


	@staticmethod
	def http_post(url, extra_headers={}, data=None):
		""" Make HTTP GET request again given URL """
		
		# Baisc Headers
		headers = {
	    	"Authorization": MyDropbox.ACCESS_TOKEN,
	    	"Content-Type": "application/json"
		}

		# Append extra headers
		for key, value in extra_headers.items():
			headers[key] = value

		# Call HTTP post method on given data
		response = requests.post(url, headers=headers, data=data)

		# Check Status Code
		if response.status_code == 200:
			return response.json()
		else:
			logging.error("Response : {}".format(response.text))
			handle_error('Status Code "{}" received for USEAGE API call : {}'.format(response.status_code
						, url))
		
		

		

		



