from flight import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class Airplane:
    collection = mongo.db.airplanes

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)
    

    @classmethod
    def update_seat_count(cls, airplane_id, seat_type, num_passengers):
        airplane = cls.get_by_id(airplane_id)
        airplane["seats"][seat_type] -= num_passengers
        return cls.update(airplane_id, airplane)
    

    @classmethod
    def get_all(cls):
        return list(cls.collection.find())
    

    @classmethod
    def update(cls, airplane_id, data):
        return cls.collection.update_one({"_id": airplane_id}, {"$set": data})
    

    @classmethod
    def get_by_id(cls, airplane_id):
        return cls.collection.find_one({"_id": airplane_id})
    

    @classmethod
    def delete(cls, airplane_id):
        return cls.collection.delete_one({"_id": airplane_id})

