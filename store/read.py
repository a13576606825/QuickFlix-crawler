'''
DB Read Service
---------------
'''
import logging
import mongo
from util import debug
from bson.objectid import ObjectId

log = logging.getLogger(__name__)

def search_by_title(collection, title):
    db = mongo.get_db()
    selected_collection = db.collection
    result_list = list(db.selected_collection.find({'itemReviewed.name': title}))
    if not result_list:
        return 0
    return result_list

'''
def read_by_id(collection, object_id):
    if not isinstance(object_id, ObjectId):
        object_id = ObjectId(object_id)
    db = mongo.get_db()
    cursor = db[collection].find({'_id': object_id})
    for document in cursor:
        return document
    log.info('No data found for id ' + str(object_id))
    ['itemReviewed']['name']
    return None


def find(collection, condition, col=None):
    db = mongo.get_db()
    cursor = db[collection].find(condition, col)
    return cursor


def query(collection, condition, col=None):
    cursor = find(collection, condition, col)
    return [item for item in cursor]


def smart_query(collection, condition):
    """
    Smart query is smart because it provide both
    """
    smart_condition = list()
    for condition_key, condition_value in condition.iteritems():
        if isinstance(condition_value, dict):
            # We do not optimize complicate conditions.
            smart_condition.append({condition_key: condition_value})
        else:
            smart_condition.append({"$or": [
                {condition_key: condition_value},
                {condition_key: None},
                {condition_key: {"$exists": False}}
            ]})
    query_condition = {"$and": smart_condition}
    debug.print_as_json(query_condition)
    return query(collection, query_condition)
'''
