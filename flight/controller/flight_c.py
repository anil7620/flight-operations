from flask import render_template, request, redirect, url_for, session, flash
from flight import flight 
import logging
from datetime import datetime
from bson.objectid import ObjectId 
from flask import jsonify 
from flight.model.admin import Admin
from flight.model.customer import Customer 
from flight.model.airplane import Airplane
from flight.model.airport import Airport
from flight.model.flight import Flight

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta

@flight.route('/admin_scheduled_flights', methods=['GET', 'POST'])
def admin_flights():
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        flight_number = request.form.get("flight_number").strip()
        airplane_id = request.form.get("airplane_id").strip()
        origin_airport = request.form.get("origin_airport").strip()
        destination_airport = request.form.get("destination_airport").strip()
        start_datetime_str = request.form.get("start_datetime").strip()
        end_datetime_str = request.form.get("end_datetime").strip()

        # Convert strings to datetime objects
        start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        # Validate start datetime is not in the past
        if start_datetime < current_datetime:
            flash("Start date and time cannot be in the past.", "error")
            return redirect(url_for('admin_flights'))
        
        if end_datetime < start_datetime:
            flash("End date and time cannot conflict with start.", "error")
            return redirect(url_for('admin_flights'))

        # Check if origin and destination airports are the same
        if origin_airport == destination_airport:
            flash("Origin and destination airports cannot be the same.", "error")
            return redirect(url_for('admin_flights'))

        # Check for conflicts
        if Flight.check_conflict(airplane_id, start_datetime, end_datetime):
            flash("The airplane is already scheduled for another flight during this time.", "error")
            return redirect(url_for('admin_flights'))

        # Get available seats from airplane
        airplane = Airplane.get_by_id(ObjectId(airplane_id))
        seats = airplane["seat_type_available"]

        seats_cost = {
            "first_class": float(request.form.get("first_class_cost").strip()),
            "business_class": float(request.form.get("business_class_cost").strip()),
            "economy_class": float(request.form.get("economy_class_cost").strip())
        }
        
        data = {
            "flight_number": flight_number,
            "airplane_id": ObjectId(airplane_id),
            "origin_airport": ObjectId(origin_airport),
            "destination_airport": ObjectId(destination_airport),
            "start_datetime": start_datetime,
            "end_datetime": end_datetime, 
            "seats": seats,
            "seats_cost": seats_cost
        }
        Flight.create(data)
        flash("Flight added successfully!", "success")
        return redirect(url_for('admin_flights'))
    
    airplanes = Airplane.get_all()
    airports = Airport.get_all()
    airports_dest = Airport.get_all()
    flights = Flight.get_all()
    for flight in flights:
        flight["from"] = Airport.get_by_id(flight["origin_airport"])["airport_name"]
        flight["to"] = Airport.get_by_id(flight["destination_airport"])["airport_name"]

    return render_template('flights/admin_manage_flights.html', airplanes=airplanes, airports=airports, flights=flights, airports_dest=airports_dest)



@flight.route('/admin_flights/<flight_id>', methods=['GET', 'POST'])
def admin_flight_edit(flight_id):
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        airplane_id = request.form.get("airplane_id").strip()
        origin_airport = request.form.get("origin_airport").strip()
        destination_airport = request.form.get("destination_airport").strip()
        start_datetime = datetime.strptime(request.form.get("start_datetime").strip(), "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(request.form.get("end_datetime").strip(), "%Y-%m-%d %H:%M")
        
        seats_cost = {
            "first_class": float(request.form.get("first_class_cost").strip()),
            "business_class": float(request.form.get("business_class_cost").strip()),
            "economy_class": float(request.form.get("economy_class_cost").strip())
        }
        
        data = {
            "airplane_id": ObjectId(airplane_id),
            "origin_airport": ObjectId(origin_airport),
            "destination_airport": ObjectId(destination_airport),
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "seats_cost": seats_cost
        }
        Flight.update(ObjectId(flight_id), data)
        flash("Flight updated successfully!", "success")
        return redirect(url_for('admin_flights'))
    
    flight = Flight.get_by_id(ObjectId(flight_id))
    airplanes = Airplane.get_all()
    airports = Airport.get_all()
    airport_dest = Airport.get_all()
    return render_template('flights/admin_edit_flight.html', flight=flight, airplanes=airplanes, airports=airports, airport_dest=airport_dest)


@flight.route('/admin_flights/delete/<flight_id>', methods=['GET'])
def admin_flight_delete(flight_id):
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    
    Flight.delete(ObjectId(flight_id))
    flash("Flight deleted successfully!", "success")
    return redirect(url_for('admin_flights'))
