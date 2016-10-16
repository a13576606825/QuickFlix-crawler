'''
Crawling Service
----------------
'''

import logging

import requests
import re

log = logging.getLogger(__name__)
regex = re.compile('(text\/html|application\/xhtml\+xml|text\/xml|application\/xml).*')


'''
Arg(s): url
Return: if html document, its text body
		else None
'''
def fetch(url):
	r = requests.head(url) # TODO implement a timeout and catch exceptions
	if regex.match(r.headers['content-type']) is None:
		return None
	else:
		r = requests.get(url) # TODO implement a timeout and catch exceptions
		return r.text

