'''
Master control class
--------------------------------------------
'''

import logging

import config
from store import store
from remote import remote

log = logging.getLogger(__name__)


''' Top Level Method '''
def start():
    # Seed URLs
    #store.queue_push('http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/')
    #store.queue_push('https://github.com')
    store.queue_push('http://www.comp.nus.edu.sg/undergraduates/cs_cs_2014_15.html')

    remote.run()
