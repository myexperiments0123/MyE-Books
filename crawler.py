import os
import sys
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import logging
import traceback
from custom_library import handle_error
from mydropbox import MyDropbox
from web_crawler import Crawler

def main():
	# Set the logging details
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		
	Crawler.loop_over_pages()


if __name__ == '__main__':
	main()
		