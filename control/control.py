'''
Master control class
--------------------------------------------
'''

import logging
import threading
import time
import multiprocessing


import config
from store import store
from remote import remote

log = logging.getLogger(__name__)


THREAD_PAUSE_TIME = 1 # seconds

''' Top Level Method '''
def start():
    store.empty_db() # TODO uncommented for now

    # Seed URLs
    urls = [
    	'http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/',
    	'http://www.empireonline.com/movies/magnificent-seven-2/review/',
    	'http://www.metacritic.com/movie/the-magnificent-seven',
    	'http://www.newyorker.com/goings-on-about-town/movies/the-magnificent-seven',
    	'http://www.nytimes.com/2016/09/23/movies/magnificent-seven-review-denzel-washington.html',
    	'http://www.avclub.com/review/magnificent-seven-gets-uninspired-remake-242722',
    	'http://variety.com/author/owen-gleiberman/'
    ] # TODO uncommented for now

    for url in urls:
        # give those urls highest priority
        store.queue_push(url, 0)

    cpu_count = multiprocessing.cpu_count()
    # TODO single thread for now
    cpu_count = 1
    print('Mutithreading Number is %s' % str(cpu_count))

    for cpu_index in range(cpu_count):
        try:
            t = threading.Thread(target=_single_crawler, args=("Thread-"+str(cpu_index),))
            t.daemon=True
            t.start()
        except:
            log.debug("Error: unable to start thread %s" % cpu_index)

    # keep the main thread alive
    while True:
        time.sleep(1)


def _single_crawler(thread_name):
    '''
    one threading function that calls remote run constantly
    '''
    while True:
        try:
            remote.run(thread_name)
        except Exception as e:
            print('[%s] (BUG!!!)Unhandled exception occurs' % thread_name)
            print(e)
        time.sleep(THREAD_PAUSE_TIME)
