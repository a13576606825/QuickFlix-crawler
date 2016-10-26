'''
DB Management
---------------
'''

import logging
import mongo
from bson.objectid import ObjectId
import pymongo

log = logging.getLogger(__name__)

COLLECTIONS = ['movies', 'queue', 'reviews','visited', 'links']

def empty_db():
    db = mongo.get_db()
    for collection in COLLECTIONS:
        db[collection].delete_many({})

def add_movie(movie_title):
    db = mongo.get_db()
    item_id = db.movies.insert_one({'title': movie_title}).inserted_id
    if item_id == 0:
        log.error("Unable to add movie title")
        return None
    return item_id


# Returns a list of all movie titles
def get_movies():
    db = mongo.get_db()
    movies = list(db.movies.find())
    if movies:
        for i, item in enumerate(movies):
            movies[i] = item['title']
    return movies

def add_review(review):
    db = mongo.get_db()

    # If movie title is not already in db.movies, add it
    movie_title = review['itemReviewed']['name'] # TODO catch exception (malformed json)
    movies = list(db.movies.find({'title': movie_title}))
    if not movies:
        add_movie(movie_title)

    # Check for duplicate reviews for the same movie
    existing_reviews = get_reviews(movie_title)
    for possible_duplicate in existing_reviews:
        if review['url'] == possible_duplicate['url']:
            log.info('Review already added into database')
            return None

    # Add review into db.reviews
    item_id = db.reviews.insert_one(review).inserted_id
    if item_id == 0:
        log.error("Unable to add review")
        return None
    return item_id

def add_outgoing_links(url, outgoing_links):
    db = mongo.get_db()
    item_id = db.links.insert_one({'key':url, 'links':outgoing_links}).inserted_id

def get_outgoing_links():
    db = mongo.get_db()
    return list(db.links.find())
    
def updatePageRank(url, rank):
    db = mongo.get_db()
    db.reviews.update_one({'url':url}, {'$set': {'rank': rank}})

# Returns a list of all reviews (json objects) for a particular movie
def get_reviews(movie_title):
    db = mongo.get_db()
    reviews = list(db.reviews.find({'itemReviewed.name': movie_title}))
    if not reviews:
        log.info("No reviews found for " + movie_title)
    return reviews


def queue_push(url, priority=1):
    db = mongo.get_db()
    item_id = db.queue.insert_one({'url': url, 'priority':priority}).inserted_id
    if item_id == 0:
        log.error("Unable to add URL into queue")
        return None
    return item_id


def queue_pop():
    db = mongo.get_db()
    MAX_PRIORITY = 2
    priority = 0

    item = db.queue.find_one_and_delete({}, sort=[('priority', pymongo.ASCENDING)])
    if item is not None:
        # db.queue.delete_one({'_id': ObjectId(item['_id'])})
        return item['url'], item['priority']
    else:
        return None, None



def add_to_visited(url):
    db = mongo.get_db()
    item_id = db.visited.insert_one({'url': url}).inserted_id
    if item_id == 0:
        log.error("Unable to add URL into visited")
        return None
    return item_id


def get_visited():
    db = mongo.get_db()
    visited = list(db.visited.find())
    if visited:
        for i, item in enumerate(visited):
            visited[i] = item['url']
    return visited
