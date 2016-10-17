'''
DB Management
---------------
'''

import logging
from store import mongo
from remote import read
from remote import write
from bson.objectid import ObjectId

log = logging.getLogger(__name__)

def insert_into_db(collection, review):
    # Call upon writing function in remote 
    # Writes the entire JSON string passed in
    item_id = remote.write.insert_one(collection, review)
    return item_id

def read_from_db(collection, field):
    # TODO: query db for items which fulfill the field
    # Field can be Movie Title, Director or Actor
    movie_title = review['itemReviewed']['name']
