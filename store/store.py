'''
DB Management
---------------
'''

import logging
import read
import write
from bson.objectid import ObjectId

log = logging.getLogger(__name__)


def add_review(review):
    item_id = write.write_review_into_db(review)
    return item_id

def get_reviews(movie_title):
    reviews = read.search_reviews_by_title(movie_title)
    if len(reviews) == 0:
        log.info("No reviews found for " + movie_title)
    return reviews

def queue_push(url):
    item_id = write.write_next_url(url)
    return item_id

def queue_pop():
    # TODO pop the first url
    url = read.read_next_urls()
    return url

def add_to_visited(url):
    item_id = write.write_visited_url(url)
    return item_id
    
def get_visited():
    visited = read.read_visited_urls()
    return visited
