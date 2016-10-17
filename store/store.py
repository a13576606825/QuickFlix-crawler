'''
DB Management
---------------
'''

import logging
import read
import write
from bson.objectid import ObjectId

log = logging.getLogger(__name__)


def write_review(review):
    item_id = write.write_review_into_db(review)
    return item_id

def read_review(movie_title):
    # please refactor such that this always returns a list, even though the list might be empty or only contain one element
    results = []
    list_of_reviews = read.search_reviews_by_title(movie_title)
    if list_of_reviews == 0:
        log.info("No reviews for the chosen movie title found")
        return results
    #for review in list_of_reviews:
        # They should all fulfill this from the function call
    #    if review['itemReviewed']['name'] == field:   
    #        results.append(review)
    return list_of_reviews

def write_queue(url):
    # Pushes a URL to said queue
    next_url = {'url': url}
    item_id = write.write_next_urls(next_url)
    return item_id

def read_queue():
    # Returns queue of URLs to visit
    # (Not sure if python has a queue DS. Otherwise a list is fine!)
    url_queue = read.read_next_urls()
    return url_queue

def write_visited(url):
    # Adds URL to said list
    previous_url = {'url': url}
    item_id = write.write_visited_url(previous_url)
    return item_id
    
def read_visited():
    # Returns list (or maybe a hashmap?) of already visited URLs
    visited_urls = read.read_visited_urls()
    return visited_urls