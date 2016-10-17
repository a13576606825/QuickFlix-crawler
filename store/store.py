'''
DB Management
---------------
'''

import logging
from store import read
from store import write
from bson.objectid import ObjectId

log = logging.getLogger(__name__)

def insert_into_db(collection, review):
    # Call upon writing function in remote 
    # Writes the entire JSON string passed in
    item_id = store.write.insert_one_into_db(collection, review)
    return item_id

def read_from_db(collection, field):
    # TODO: Query with Director or Actor (?)
    # Takes in title and searches the collection for relevant urls
    results = []
    list_of_reviews = store.read.search_by_title(collection, field)
    if list_of_reviews == 0:
        log.info("No reviews for the chosen movie title found")
        return 0
    for review in list_of_reviews:
        # They should all fulfill this from the function call
        if review['itemReviewed']['name'] == field:   
            results.append(review)
    return results
