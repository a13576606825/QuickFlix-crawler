'''
DB Write Service
---------------
'''

import logging
from store import mongo
from bson.objectid import ObjectId

log = logging.getLogger(__name__)

# Should be handled in the parser section, temporarily here for testing
def check_duplicates(collection, data):
    for doc in collection.find({}):
        print(doc)
        return collection.find(data)
    return 0


def insert_one(collection, data):
    db = mongo.get_db()
    selected_collection = db.collection
    existing_id = check_duplicates(selected_collection, data)
    if existing_id != 0:
        print('Specified URL already exists in database')
        return 0
    result_id = selected_collection.insert_one(data).inserted_id
    return result_id

'''   Unused functionalities (as of current implementations; kept just in case for now'''
"""   
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