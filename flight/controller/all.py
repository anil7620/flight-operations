from flask import render_template, request, redirect, url_for, session, flash
from flight import flight 
import logging
from datetime import datetime
from bson.objectid import ObjectId 
from flask import jsonify 
from flight.model.admin import Admin
from flight.model.customer import Customer 
from flight.model.flight import Flight
from flight.model.airport import Airport
from flight.model.reservation import Reservation
from datetime import timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@flight.route('/', methods=['GET', 'POST'])
def home():
    is_logged_in = 'user_id' in session
    return render_template('index.html', is_logged_in=is_logged_in)

@flight.route('/search', methods=['GET'])
def search_flights():
    departure = request.args.get('departure')
    arrival = request.args.get('arrival')
    date = request.args.get('date')

    # Fetch airport IDs based on names
    departure_airport = Airport.find_one({'airport_name': departure})
    arrival_airport = Airport.find_one({'airport_name': arrival})

    if departure_airport and arrival_airport:
        departure_id = departure_airport['_id']
        arrival_id = arrival_airport['_id']

        # Fetch flights from the database based on search criteria
        flights = Flight.find({
            'origin_airport': ObjectId(departure_id),
            'destination_airport': ObjectId(arrival_id),
            'start_datetime': {
                '$gte': datetime.strptime(date, "%Y-%m-%d"),
                '$lt': datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
            }
        })

        # Add airport names to the flight data
        for flight in flights:
            flight['departure_name'] = departure_airport['airport_name']
            flight['arrival_name'] = arrival_airport['airport_name']

        is_logged_in = 'user_id' in session
        return render_template('index.html', flights=flights, is_logged_in=is_logged_in)
    else:
        flash("Invalid departure or arrival airport.")
        return redirect(url_for('home'))


@flight.route('/api/airports', methods=['GET'])
def get_airports():
    airports = Airport.get_all()
    return jsonify([{
        '_id': str(airport['_id']),
        'airport_name': airport['airport_name'],
        'state': airport['state']
    } for airport in airports])
 





@flight.route('/book/<flight_id>', methods=['GET'])
def book_flight(flight_id):
    if 'user_id' not in session:
        return redirect(url_for('customer_login', next=url_for('book_flight', flight_id=flight_id)))
    
    flight = Flight.get_by_id(ObjectId(flight_id))
    if flight:
        flight['departure_name'] = Airport.get_by_id(flight['origin_airport'])['airport_name']
        flight['arrival_name'] = Airport.get_by_id(flight['destination_airport'])['airport_name']
        return render_template('customer/cust_booking.html', flight=flight, is_logged_in=True)
    else:
        flash("Flight not found.")
        return redirect(url_for('home'))


# @flight.route('/book/<flight_id>/<seat_type>', methods=['GET', 'POST'])
# def book_seat(flight_id, seat_type):
#     if 'user_id' not in session:
#         return redirect(url_for('customer_login', next=url_for('book_seat', flight_id=flight_id, seat_type=seat_type)))

#     flight = Flight.get_by_id(ObjectId(flight_id))
#     if not flight:
#         flash("Flight not found.")
#         return redirect(url_for('home'))

#     if request.method == 'POST':
#         # Process the booking here (save to database, etc.)
#         flash(f"Successfully booked {seat_type.replace('_', ' ')} seat on flight {flight_id}")
#         return redirect(url_for('customer_dashboard'))

#     seat_cost = flight['seats_cost'].get(seat_type, 0)
#     return render_template('customer/confirm_booking.html', flight=flight, seat_type=seat_type, seat_cost=seat_cost)
