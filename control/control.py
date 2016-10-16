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

    data = remote.crawler.fetch('http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/')
    log.info(data)
