from flight import flight
from flight.controller import admin, all, customer, airport, airplane, flight_c, payments
if __name__ == "__main__":
    flight.run(host='0.0.0.0', port=5000, debug=True)