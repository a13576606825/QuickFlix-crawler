'''
Crawling Service
----------------
'''

import logging

from store import store

import requests
import re
import json
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)
regex_html = re.compile('(text\/html|application\/xhtml\+xml).*')
regex_host = re.compile('http(|s):\/\/.+?\/')
regex_json = re.compile('{.*}')


def _thread_log(thread_name):
	'''
	return a logger that has thread_name as prefix
	'''
	def write_to_log(line):
		print("[]"+str(thread_name)+"] " + line)
	return write_to_log

# KIV
'''
# Check that stored review can be retrieved
reviews_in_db = store.get_reviews(movie_title)
if len(reviews_in_db) == 0:
	t_print('No reviews found for ' + movie_title)
else:
	for rev in reviews_in_db:
		t_print('Found a review by ' + rev['author'][0]['name'])

#url = 'http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/'
'''
def run(thread_name):
	t_print = _thread_log(thread_name)
	t_print('\n=== Running an instance of remote ================')

	# Pop URL from queue
	t_print('> Getting next url from queue')
	url = store.queue_pop()
	# url = 'http://variety.com/author/owen-gleiberman/'
	if url is None:
		t_print('  > No urls in queue')
		t_print('  > Exiting')
		return

	# Check if URL is already visited
	t_print('> Checking if url is already visited')
	visited = store.get_visited()
	if url in visited:
		t_print('  > Already visited ' + url)
		t_print('  > Exiting')
		return

	# Fetch domain + html from host
	t_print('> Fetching info from ' + url)
	domain_html = fetch_html(url)
	if domain_html is None:
		t_print('  > Unable to obtain html from host')
		t_print('  > Exiting')
		return

	# Parse review and add to database
	t_print('> Searching for review in html content')
	review = parse_review(domain_html['html'])
	if review is None:
		t_print('  > Page does not contain a movie review json')
	else:
		movie_title = review['itemReviewed']['name']
		store.add_review(review)
		t_print('  > Page contains a movie review json for ' + movie_title)

	# Parse URLs and add to queue
	t_print('> Searching for urls in html content')
	urls = parse_urls(domain_html)
	if not urls:
		t_print('  > No urls found')
	else:
		t_print('  > Adding ' + str(len(urls)) + ' urls to queue')
		for url in urls:
			store.queue_push(url)

	t_print('> Success')


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
			review = json.loads(review_string) # TODO catch exception

			if review.has_key('@type') and review.has_key('itemReviewed') and review['itemReviewed'].has_key('@type') and review['@type'] == 'Review' and review['itemReviewed']['@type'] == 'Movie':
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
