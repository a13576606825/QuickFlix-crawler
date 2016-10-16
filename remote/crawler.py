'''
Crawling Service
----------------
'''

import logging

import requests
import re
import json
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)
regex_html = re.compile('(text\/html|application\/xhtml\+xml).*')
regex_json = re.compile('{.*}')


'''
Arg(s): url

if host gives a html document, return its text body
else return None
'''
def fetch(url):
	r = requests.head(url) # TODO implement a timeout and catch exceptions

	if regex_html.match(r.headers['content-type']) is None:
		return None
	else:
		r = requests.get(url) # TODO implement a timeout and catch exceptions
		return r.text

'''
Arg(s): text body of html document

if movie review json exists, return the json object
else return None
'''
def parseReview(html):
	soup = BeautifulSoup(html, 'html.parser')

	for script_block in soup.find_all('script', attrs={'type': 'application/ld+json'}):
		review_string = script_block.string
		find_json = regex_json.search(review_string)

		if find_json is not None:
			review_string = find_json.group(0)
			review = json.loads(review_string) # TODO catch exception

			if review.has_key('@type') and review.has_key('itemReviewed') and review['itemReviewed'].has_key('@type') and review['@type'] == 'Review' and review['itemReviewed']['@type'] == 'Movie':
				return review;
	
	return None

