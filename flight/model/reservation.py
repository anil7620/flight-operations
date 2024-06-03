from flight import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class Reservation:
    collection = mongo.db.reservations

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)
    

    @classmethod
    def delete(cls, reservation_id):
        return cls.collection.delete_one({"_id": ObjectId(reservation_id)})
    

    @classmethod
    def get_by_id(cls, reservation_id):
        return cls.collection.find_one({"_id": ObjectId(reservation_id)})
    

    @classmethod
    def update_payment_id(cls, reservation_id, payment_id):
        return cls.collection.update_one(
            {"_id": ObjectId(reservation_id)},
            {"$set": {"payment_id": ObjectId(payment_id)}}
        )


    @classmethod
    def get_bookings(cls, user_id):
        return list(cls.collection.find({"user_id": user_id}))