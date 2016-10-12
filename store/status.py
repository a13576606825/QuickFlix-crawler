'''
DB Service for various status data
----------------------------------
'''

import logging
import store.read
import store.write


log = logging.getLogger(__name__)


def _read_document(key):
    records = store.read.query('status', {'key': key})
    for record in records:
        return record


def read(key):
    record = _read_document(key)
    if record is not None:
        return record['value']
    else:
        log.info('Unable to read status of ' + key)


def save(key, value):
    record = _read_document(key)
    if record is not None:
        store.write.update_by_id('status', record['_id'], {'value': value})
    else:
        log.info('Create new status of ' + key)
        store.write.insert_one('status', {'key': key, 'value': value})

def remove(key):
    record = _read_document(key)
    if record is not None:
        store.write.delete_by_id('status', record['_id'])
