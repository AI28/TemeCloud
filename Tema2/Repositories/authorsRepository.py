from Models.Author import *
from ORM.persistence import *

import bson.json_util

authorsCollection = None

def get_coll_instance():

    global authorsCollection
    if authorsCollection is None:
        authorsCollection = CollectionBuilder.create_collection("Authors")

    return authorsCollection

def get(query=None):

    authorsCollection = get_coll_instance()
    result = None

    if query is None:

        try:
            result = authorsCollection.get_collection()
            if result == None:
                result = False
            else:
                result = bson.json_util.dumps(result)
        except ValueError as ve:
            result = False
            print(ve)
        finally:
            return result

    else:

        try:
            result = authorsCollection.find_one(query)
            if result == None:
                result = False
            else:
                result = bson.json_util.dumps(result)
        except ValueError as ve:
            result = False
            print(ve)
        finally:
            return result

def delete(query):

    authorsCollection = get_coll_instance()
    result = None
    
    result = authorsCollection.delete_item(query)

    if result.deleted_count == 0:
        return False
    else:
        return True


def post(body):

    authorsCollection = get_coll_instance()
    result = None

    try:
        next_id = authorsCollection.get_max("id")
        body["id"] = str(int(next_id["id"]) + 1)
        result = authorsCollection.insert_item(body)
    except ValueError as ve:
        return False

    return bson.json_util.dumps(result), body["id"]


def put(author_id, body):

    authorsCollection = get_coll_instance()
    result = None
    body["id"] = author_id

    if authorsCollection.find_one({"id":author_id}) is None:
        try:
            body["id"] = author_id
            result = authorsCollection.insert_item(body)
        except ValueError as ve:
            result = False
            return bson.json_util.dumps(result)

    else:
        try:
            query = {"id":author_id}
            authorsCollection.delete_item(query)
            result = authorsCollection.insert_item(body)
        except ValueError as ve:
            result = False
            return bson.json_util.dumps(result)

    print(result)
    return bson.json_util.dumps(result)