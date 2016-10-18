'''
DB Management
---------------
'''

import logging
import mongo
from bson.objectid import ObjectId

log = logging.getLogger(__name__)


def add_review(review):
    db = mongo.get_db()
    item_id = db.reviews.insert_one(review).inserted_id
    if item_id == 0:
        log.error("Unable to add selected review")
        return 0
    return item_id


def get_reviews(movie_title):
    db = mongo.get_db()
    reviews = list(db.reviews.find({'itemReviewed.name': movie_title}))
    if not reviews:
        reviews = []
        log.info("No reviews found for " + movie_title)
    return reviews


def queue_push(url):
    db = mongo.get_db()
    item_id = db.queue.insert_one({'url': url}).inserted_id
    if item_id == 0:
        log.error("Unable to add selected URL into queue")
        return 0
    return item_id


def queue_pop():
    db = mongo.get_db()
    item = db.queue.find_one()
    if item is None:
        return None
    else:
        db.queue.delete_one({'_id': ObjectId(item['_id'])})
        return item['url']


def add_to_visited(url):
    db = mongo.get_db()
    item_id = db.visited.insert_one({'url': url}).inserted_id
    if item_id == 0:
        log.error("Unable to add selected URL into visited")
        return 0
    return item_id


def get_visited():
    db = mongo.get_db()
    visited = list(db.visited.find())
    if visited:
        for i, item in enumerate(visited):
            visited[i] = item['url']
    return visited
