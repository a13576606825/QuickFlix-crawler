'''
Crawling Service
----------------
'''

import logging

log = logging.getLogger(__name__)

def remote():
	''' TODO
	- Pop URLs from the queue
	- Visit it (or not)
		`-> Parse the review (if the page has one)
		`-> Parse new URLs and add them to the queue
	'''
