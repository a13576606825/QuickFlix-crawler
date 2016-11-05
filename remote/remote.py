'''
Crawling Service
----------------
'''

import logging
urllib3_logger = logging.getLogger('requests')
urllib3_logger.setLevel(logging.CRITICAL)

from store import store

import requests
import re
import json
import urllib2
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)
regex_html = re.compile('(text\/html|application\/xhtml\+xml).*')
regex_host = re.compile('http(|s):\/\/.+?\/')
regex_json = re.compile('{[\s\S]*}')

def check_validity(url):
	domain_html = fetch_html(url)
	if domain_html is None:
		return False
	review = parse_review(domain_html['html'])
	if review is not None:
		return True

# return a logger that has thread_name as prefix
def _thread_log(thread_name):
	def write_to_log(line):
		print("["+str(thread_name)+"] " + line)
	return write_to_log

def run(thread_name):
	t_print = _thread_log(thread_name)

	# To easily trace when a new thread begins
	t_print('==========')

	# Pop URL from queue
	url, url_priority = store.queue_pop()
	if url is None:
		t_print('> No urls in queue')
		return

	# Check if URL is already visited
	visited = store.get_visited()
	if url in visited:
		t_print('> Already visited ' + url)
		return

	# Fetch domain + html from host
	domain_html = fetch_html(url)
	if domain_html is None:
		t_print('> Unable to obtain html from ' + url)
		return

	this_domain = domain_html['domain']
	this_html = domain_html['html']
	if not store.should_visit_domain(this_domain):
		t_print('> this_domain should not be fetched: ' + this_domain)
		return
	# Parse review and URLs
	review = parse_review(this_html)
	urls = parse_urls(domain_html)
	found_review = review is not None
	store.update_visited_domain(domain_html['domain'], found_review)
	# Add review to database
	if not found_review:
		t_print('> Page does not contain a movie review json')
	else:
		movie_title = review['itemReviewed']['name']
		t_print('> Page contains a movie review json for ' + movie_title)
		if 'url' not in review:
			review['url'] = url
		if store.add_review(review):
			t_print('> Added review successfully')
			# Add all outgoing links
			store.add_outgoing_links(url, urls)

	# Add URLs to queue
	if not urls:
		t_print('> No urls found')
	else:
		t_print('> Adding ' + str(len(urls)) + ' urls to queue')
		next_url_priority = 1 if review is not None else (url_priority+1)
		for url in urls:
			store.queue_push(url, next_url_priority)

'''
Arg(s): url

if host responds with a html document, return dictionary containing domain + text body of html document
else return None
'''
def fetch_html(url):
	# Add URL to visited
	store.add_to_visited(url)

	# Exception handling
	try:
		# Initiate connection, defer downloading of response body
		r = requests.get(url, stream=True)
	#except requests.exceptions.ConnectionError:
	#except requests.exceptions.Timeout:
		# TODO Reinsert into queue to set up for a retry, don't add to visited?
		# http://docs.python-requests.org/en/master/api/#exceptions
		# store.queue_push(url)
	except requests.exceptions.RequestException as e:
		log.info('Connection error')
		return None

	# Detect redirects
	if url != r.url:
		log.info('Redirect detected: ' + r.url)
		store.add_to_visited(r.url)

	# Check if content-type is html
	if regex_html.match(r.headers['content-type']) is None:
		log.info('Content-type is not html')
		r.close()
		return None

	# Extract domain from host url
	matches = regex_host.match(r.url)
	if matches is None:
		log.info('Host is not http/https')
		r.close()
		return None

	# Download response content
	domain = matches.group(0)

	html = r.text
	r.close()
	return {'domain': domain, 'html': html}

'''
Arg(s): text body of html document

if movie review json exists, return the json object
else return None
'''
def parse_review(html):
	soup = BeautifulSoup(html, 'html.parser')
	for script_block in soup.find_all('script', attrs={'type': 'application/ld+json'}):
		review_string = script_block.string
		find_json = regex_json.search(review_string)

		if find_json is not None:
			review_string = find_json.group(0)
			try:
				review = json.loads(review_string)
			except ValueError:
				log.warning('parse review value error')
				return None

			# Assumes that each page doesn't have more than one review
			if review.has_key('@type') and review.has_key('itemReviewed') and review['itemReviewed'].has_key('name') and review['itemReviewed'].has_key('@type') and review['@type'] == 'Review' and review['itemReviewed']['@type'] == 'Movie':
				return review

	return None

'''
Arg(s): dictionary containing domain + text body of html document

returns a list that contains all (processed) urls in the html document
'''
def parse_urls(domain_html):
	domain = domain_html['domain']
	soup = BeautifulSoup(domain_html['html'], 'html.parser')
	urls = []
	for a in soup.find_all('a'):
		link = a.get('href')

		if link is None:
			continue
		elif link.startswith('/'):
			urls.append(domain + link[1:])
		elif link.lower().startswith('http://') or link.lower().startswith('https://'):
			urls.append(link)

	return urls
