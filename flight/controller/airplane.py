from flask import render_template, request, redirect, url_for, session, flash
from flight import flight 
import logging
from datetime import datetime
from bson.objectid import ObjectId 
from flask import jsonify 
from flight.model.admin import Admin
from flight.model.customer import Customer 
from flight.model.airplane import Airplane

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@flight.route('/admin_airplanes', methods=['GET', 'POST'])
def admin_airplanes():
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST': 
        flight_name = request.form.get("flight_name").strip()
        airline = request.form.get("airline").strip()
        seat_type_available = {
            "first_class": int(request.form.get("first_class").strip()),
            "business_class": int(request.form.get("business_class").strip()),
            "economy_class": int(request.form.get("economy_class").strip())
        }
        
        data = { 
            "flight_name": flight_name,
            "airline": airline,
            "seat_type_available": seat_type_available
        }
        Airplane.create(data)
        flash("Airplane added successfully!", "success")
        return redirect(url_for('admin_airplanes'))
    
    airplanes = Airplane.get_all()
    return render_template('airplanes/admin_manage_airplanes.html', airplanes=airplanes)


@flight.route('/admin_airplanes/<airplane_id>', methods=['GET', 'POST'])
def admin_airplane_edit(airplane_id):
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        flight_name = request.form.get("flight_name").strip()
        airline = request.form.get("airline").strip()
        seat_type_available = {
            "first_class": int(request.form.get("first_class").strip()),
            "business_class": int(request.form.get("business_class").strip()),
            "economy_class": int(request.form.get("economy_class").strip())
        }
        
        data = {
            "flight_name": flight_name,
            "airline": airline,
            "seat_type_available": seat_type_available
        }
        Airplane.update(ObjectId(airplane_id), data)
        flash("Airplane updated successfully!", "success")
        return redirect(url_for('admin_airplanes'))
    
    airplane = Airplane.get_by_id(ObjectId(airplane_id))
    return render_template('airplanes/admin_edit_airplane.html', airplane=airplane)


@flight.route('/admin_airplanes/delete/<airplane_id>', methods=['GET'])
def admin_airplane_delete(airplane_id):
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('admin_login'))
    
    Airplane.delete(ObjectId(airplane_id))
    flash("Airplane deleted successfully!", "success")
    return redirect(url_for('admin_airplanes'))
