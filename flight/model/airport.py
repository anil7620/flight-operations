from flight import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class Airport:
    collection = mongo.db.airports

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)
    

    @classmethod
    def get_by_id(cls, airport_id):
        return cls.collection.find_one({"_id": airport_id})
    

    @classmethod
    def update(cls, airport_id, data):
        return cls.collection.update_one({"_id": airport_id}, {"$set": data})
    

    @classmethod
    def delete(cls, airport_id):
        return cls.collection.delete_one({"_id": airport_id})
    


    @classmethod
    def get_all(cls):
        return cls.collection.find()

    @classmethod
    def find_one(cls, query):
        return cls.collection.find_one(query)
    

    @classmethod
    def get_airportname(cls, airport_id):
        return cls.collection.find_one({"_id": airport_id}, {"name": 1})
