import logging
import config
from pymongo import MongoClient

log = logging.getLogger(__name__)

_db = None


def get_db():
    global _db
    if _db is None:
        log.info('No database connection yet, trying to establish new connection.')
        host = config.read('basic', 'mongo-db-host')
        port = config.read('basic', 'mongo-db-port')
        client = MongoClient(host=host, port=port)
        #client.fim.authenticate('fim', 'fim', mechanism='SCRAM-SHA-1')
        # collection name is crawler
        _db = client.crawler
    return _db
