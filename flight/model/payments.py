from flight import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class Payment:
    collection = mongo.db.payments

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)
    
