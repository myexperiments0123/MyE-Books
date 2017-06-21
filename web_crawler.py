import sys
import os
import json
import logging
import traceback
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from custom_library import handle_error
from config_parser import Config

class Crawler(object):
	""" Web crawler for parsing the web """

	# Create Static Variables from CONFIG
	for key, value in Config.WEBSITE.items():
		locals()[key] = value	

	@staticmethod
	def get_html_of_url(url, return_json=False):
		""" Returns the HTML content or JSON object of the given URL """

		# Invoke HTTP GET Method on given URL 
		response = requests.get(url)

		# Validate the Returned Status Code of request
		if response.status_code != 200 :
			handle_error("Status Code {} is retured for url hit : {}".format(url))		
		else:
			# Return the HTML Content or JSON based on check return_json
			return response.json() if return_json else response.text

	@staticmethod
	def get_bs_parser(url):
		""" Return BeautifulSoup Parser for URL """	

		# Pass the returned HTML content to  BeautifulSoup and return the parser
		return BeautifulSoup(Crawler.get_html_of_url(url), 'html.parser')

	@staticmethod
	def get_last_page_num():
		""" Returns the last page num of the given website by parsing pagination"""

		# Get Parser for the Given URL in the CONFIG to parse paigantion by visiting first page
		parser = Crawler.get_bs_parser(Crawler.URL.format(1))

		# Find the pagination tag using Identifier specifed in CONFIG
		tag_identifier 	= {
			Crawler.TAGS['paging_tag']['attrib'] : Crawler.TAGS['paging_tag']['value']
		}
		paginator_tag 	= parser.find(Crawler.TAGS['paging_tag']['tag'], tag_identifier)

		# Get the last page by using find all and list reverse indexing
		last_page_num = paginator_tag.find_all('li')[-1].text.strip()

		# Convert Page num from STRING to INT
		try:
			last_page_num = int(last_page_num)
		except ValueError as err:
			handle_error('An error occured while converting the last page string "{}" to int : '\
				.format(last_page_num)
				, err)
		else:
			return last_page_num

	@staticmethod
	def loop_over_pages():
		last_page = Crawler.get_last_page_num()
		book_details = []
		for page in range(1, last_page + 1):			
			parser = Crawler.get_bs_parser(Crawler.URL.format(page))
			all_books_div_identifier = {
				Crawler.TAGS['all_books_tag']['attrib'] : Crawler.TAGS['all_books_tag']['value']
			}
			books = parser.find(Crawler.TAGS['all_books_tag']['tag'], all_books_div_identifier)
			book_identifier = {
				Crawler.TAGS['book_tag']['attrib'] : Crawler.TAGS['book_tag']['value']
			}
			for book in books.find_all(Crawler.TAGS['book_tag']['tag'], book_identifier):
				img = book.find('img')
				book_info = Crawler.extract_book(book)
				pprint(book_info)
			break

	@staticmethod
	def extract_book(book):
		img = book.find('img')
		a 	= book.find('a')
		return {
			"name" : img.get('alt').strip(),
			"slug" : img.get('src').strip().split('books/')[-1].replace('jpg','zip'),
			"book_id" : int(a.get('href').strip().split('/')[-1]),
		}