'''
Master control class
--------------------------------------------
'''

import logging

import store
import config

log = logging.getLogger(__name__)
TESTING = False

''' Top Level Method'''
def start():
    store.write.insert_one('test', {'number':1})
