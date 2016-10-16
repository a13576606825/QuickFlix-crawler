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

    # TODO
    url = 'http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/';
    html = remote.crawler.fetch(url)
    review = remote.crawler.parseReview(html)
    if review is None:
    	log.info('Page does not contain a movie review json')
    else:
    	log.info(review['author'][0]['name'])
