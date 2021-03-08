from ORM.persistence import *

import bson.json_util

booksCollection = None

def get_coll_instance():

    global booksCollection
    if booksCollection is None:
        booksCollection = CollectionBuilder.create_collection("Books")

    return booksCollection

def get(query=None):

    booksCollection = get_coll_instance()
    result = None

    if query is None:

        try:
            result = booksCollection.get_collection()
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
            result = booksCollection.find_one(query)
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

    booksCollection = get_coll_instance()
    result = None
    
    result = booksCollection.delete_item(query)

    if result.deleted_count == 0:
        return False
    else:
        return True


def post(body):

    booksCollection = get_coll_instance()
    result = None

    try:
        next_id = booksCollection.get_max("id")
        body["id"] = str(int(next_id["id"]) + 1)
        result = booksCollection.insert_item(body)
    except ValueError as ve:
        return False

    return bson.json_util.dumps(result)


def put(book_id, body):

    booksCollection = get_coll_instance()
    result = None
    body["id"] = book_id

    if booksCollection.find_one({"id":book_id}) is None:
        try:
            body["id"] = book_id
            result = booksCollection.insert_item(body)
        except ValueError as ve:
            result = False
            return bson.json_util.dumps(result)

    else:
        try:
            query = {"id":book_id}
            booksCollection.delete_item(query)
            result = booksCollection.insert_item(body)
        except ValueError as ve:
            result = False
            return bson.json_util.dumps(result)

    print(result)
    return bson.json_util.dumps(result)