import pymongo
import json

class Jsonizer:

    def to_dict(self, obj):
        return {key:obj.__getattribute__(key) for key in dir(obj) if key[0:2] != "__"}
    
    def to_json(self, obj):
        return json.dumps(self.__to_dict(obj))


class ObjectToDocument:

    def prepare_query(object, query_type="find"):

        object_dict = Jsonizer.to_dict(object)
        
        if type in ["find", "delete"]:
            return json.dumps({"_id":object_dict["_id"]})
        

class DatabaseConn:

    database_conn = None

    def get_db_conn(self):

        if self.database_conn is not None:
            return self.database_conn
        else:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client["HW2-Cloud"]
            self.database_conn = db

            return self.database_conn

class Collection:

    def __init__(self, collection):

        self.db_conn = DatabaseConn().get_db_conn()
        self.collection = self.db_conn[collection]
        self.dropped = False

    def find_one(self, query):
        
        result = None

        if self.dropped is False:
            result = self.collection.find_one(query)
            return result
        else:
            raise ValueError("Collection is dropped.")

    def get_max(self, field):

        result = None

        if self.dropped is False:
            result = self.collection.find_one({},{field:1}, sort=[('id', pymongo.DESCENDING)])
            return result
        else:
            raise ValueError("Collection is dropped.")

    def delete_collection(self):

        if self.dropped is False:
            self.collection.delete_many({})
            self.collection.drop()

            self.dropped = True
        else:
            raise ValueError("Collection is dropped.")

    def insert_item(self, item):
        
        result = -1
        if self.dropped is False:
            result = self.collection.insert_one(item).inserted_id
        else:
            raise ValueError("Collection is dropped.")

        return result

    def delete_item(self, query):

       if self.dropped is False: 
           return self.collection.delete_one(query) 
       else:
           raise ValueError("Collection is dropped.")


    def get_collection(self):

        if self.dropped is False:
            return self.collection.find()
        else:
            raise ValueError("Collection is dropped.")



class CollectionBuilder:

    def create_collection(collection_name):
        return Collection(collection_name)