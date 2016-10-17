'''
Master control class
--------------------------------------------
'''

import logging

import config

log = logging.getLogger(__name__)


''' Top Level Method '''
def start():
    from remote import remote
    remote.run()
