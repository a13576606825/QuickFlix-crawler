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
    # Seed URLs
    # store.empty_db()

    urls = [
    'http://variety.com/2016/film/reviews/the-magnificent-seven-review-toronto-film-festival-denzel-washington-chris-pratt-1201854625/',
    'http://www.empireonline.com/movies/magnificent-seven-2/review/'
    ]
    for url in urls:
        # give those urls highest priority
        store.queue_push(url, 0)

    #store.queue_push('https://github.com')
    # store.queue_push('http://www.comp.nus.edu.sg/undergraduates/cs_cs_2014_15.html')

    cpu_count = multiprocessing.cpu_count()
    # cpu_count = 1
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
        except:
            print('[%s] (BUG!!!)Unhandled exception occurs' % thread_name)
        time.sleep(THREAD_PAUSE_TIME)
