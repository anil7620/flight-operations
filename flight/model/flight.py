from flight import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
class Flight:
    collection = mongo.db.flights

    @classmethod
    def create(cls, data):
        return cls.collection.insert_one(data)
    

    @classmethod
    def get_destination_airport(cls, flight_id):
        flight = cls.get_by_id(ObjectId(flight_id))
        if flight:
            return flight['destination_airport']
        else:
            raise ValueError("Flight not found")
    
    @classmethod
    def update_seat_count(cls, flight_id, seat_type, num_passengers):
        flight = cls.get_by_id(ObjectId(flight_id))
        if flight and seat_type in flight['seats']:
            new_seat_count = flight['seats'][seat_type] - num_passengers
            if new_seat_count >= 0:
                flight['seats'][seat_type] = new_seat_count
                return cls.update(ObjectId(flight_id), {"seats": flight['seats']})
            else:
                raise ValueError("Not enough seats available")
        else:
            raise ValueError("Invalid seat type or flight not found")
    

    @classmethod
    def update(cls, flight_id, data):
        return cls.collection.update_one({"_id": flight_id}, {"$set": data})
    

    @classmethod
    def get_by_id(cls, flight_id):
        return cls.collection.find_one({"_id": flight_id})
    

    @classmethod
    def delete(cls, flight_id):
        return cls.collection.delete_one({"_id": flight_id})
    

    @classmethod
    def get_all(cls):
        return list(cls.collection.find())
    

    @classmethod
    def find(cls, query):
        return list(cls.collection.find(query))