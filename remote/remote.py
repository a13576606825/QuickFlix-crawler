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

# KIV
'''
# Check that stored review can be retrieved
reviews_in_db = store.get_reviews(movie_title)
if len(reviews_in_db) == 0:
	print('No reviews found for ' + movie_title)
else:
	for rev in reviews_in_db:
		print('Found a review by ' + rev['author'][0]['name'])

#url = 'http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/'
'''

def run():
	log.info('Running an instance of remote')

	# Pop URL from queue and check if already visited
	url = store.queue_pop()
	if url is None:
		return
	visited = store.get_visited()
	if url is in visited: # TODO
		return

	# Fetch html from host and add URL to visited
	html = fetch_html(url) # TODO catch exception
	store.add_to_visited(url)

	# Parse review and add to database
	review = parse_review(html)
	if review is None:
		print('\nPage does not contain a movie review json')
	else:
		movie_title = review['itemReviewed']['name']
		print('\nPage contains a movie review json for ' + movie_title)
		store.add_review(review)

	# Parse URLs and add to queue
	urls = parse_urls(html)
	if len(urls) == 0:
		print('No urls found')
	else:
		for url in urls:
			store.queue_push(url)


'''
Arg(s): url

if host responds with a html document, return its text body (prepended with the host domain)
else return None
'''
def fetch_html(url):
	r = requests.head(url) # TODO implement a timeout and catch exceptions

	if regex_html.match(r.headers['content-type']) is None:
		return None
	else:
		r = requests.get(url) # TODO implement a timeout and catch exceptions
		host = regex_host.match(r.url).group(0)
		return host + '\n' + r.text


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
Arg(s): text body of html document (with the host domain as the first line)

returns a dictionary that contains all (processed) urls in the html document
'''
def parse_urls(html):
	soup = BeautifulSoup(html, 'html.parser')
	host = html.split('\n', 1)[0]
	urls = []

	for a in soup.find_all('a'):
		link = a.get('href')

		if link is None:
			continue
		elif link.startswith('/'):
			urls.append(host + link[1:])
		elif link.lower().startswith('http://') or link.lower().startswith('https://'):
			urls.append(link)

	return urls
