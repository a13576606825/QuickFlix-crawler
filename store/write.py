'''
DB Write Service
---------------
'''

import logging
from bson.objectid import ObjectId
from . import mongo

log = logging.getLogger(__name__)


def insert_one(collection, data):
    db = mongo.get_db()
    insert_result = db[collection].insert_one(data)
    return insert_result.inserted_id


def insert_many(collection, list_of_data):
    if len(list_of_data) == 0:
        return None
    db = mongo.get_db()
    insert_result = db[collection].insert_many(list_of_data)
    return insert_result.inserted_ids


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
