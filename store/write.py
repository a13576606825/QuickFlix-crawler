'''
DB Write Service
---------------
'''

import logging
import mongo
from bson.objectid import ObjectId

log = logging.getLogger(__name__)

def write_review_into_db(review):
    db = mongo.get_db()
    result_id = db.reviews.insert_one(data).inserted_id
    if result_id == 0:
        log.error("Unable to add selected review into database")
        return 0
    return result_id

def write_next_urls(url):
    db = mongo.get_db()
    result_id = db.queue.insert_one(url).inserted_id
    if result_id == 0:
        log.error("Unable to add selected URL into queue")
        return 0
    return result_id

def write_visited_url(url):
    db = mongo.get_db()
    result_id = db.visited.insert_one(url).inserted_id
    if result_id == 0:
        log.error("Unable to add selected URL into list")
        return 0
    return result_id    

''' Unused functionalities (as of current implementations; kept just in case for now '''
""" 
    
    #existing_id = check_duplicates(selected_collection, data)
        #if existing_id != 0:
        #    print('Specified URL already exists in database')
        #    return 0
          
def check_duplicates(collection, data):
    for doc in collection.find({}):
        print(doc)
        return collection.find(data)
    return 0

def insert_many(collection, list_of_data):
    if len(list_of_data) == 0:
        return None
    db = mongo.get_db()
    selected_collection = db.collection
    result_id = selected_collection.insert_many(list_of_data).inserted_id
    print(result_id)
    return result_id


def update_by_id(collection, object_id, data):
    if not isinstance(object_id, ObjectId):
        object_id = ObjectId(object_id)
    db = mongo.get_db()
    result = db[collection].update_one(
        {"_id": object_id},
        {"$set": data}
    )
    return result.matched_count == 1


def delete_by_id(collection, object_id):
    if not isinstance(object_id, ObjectId):
        object_id = ObjectId(object_id)
    db = mongo.get_db()
    delete_result = db[collection].delete_one({'_id': object_id})
    return delete_result.deleted_count == 1


def delete_by_condition(collection, condition):
    db = mongo.get_db()
    return db[collection].delete_many(condition)
"""
