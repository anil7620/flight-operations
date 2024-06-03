from flask import Flask
from flask_pymongo import PyMongo

flight = Flask(__name__)
flight.config["MONGO_URI"] = "mongodb://localhost:27017/flight-operations"
flight.secret_key = "notokenneeded"
mongo = PyMongo(flight)    

flight.jinja_env.globals.update(str=str)


if __name__ == "__main__":
    flight.run()