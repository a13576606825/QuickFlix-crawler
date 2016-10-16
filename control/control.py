'''
Master control class
--------------------------------------------
'''

import logging

import config
import remote
import store

log = logging.getLogger(__name__)


''' Top Level Method'''
def start():
    #store.write.insert_one('test', {'number':1})

    # fetch_html
    url = 'http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/'
    html = remote.crawler.fetch_html(url) # TODO catch exception

    # parse_review
    review = remote.crawler.parse_review(html)
    if review is None:
    	print('Page does not contain a movie review json')
    else:
    	print(review['author'][0]['name'])

    # parse_urls
	urls = remote.crawler.parse_urls(html)
	if len(urls) == 0: print('No urls found')
	for url in urls:
		print(url)
