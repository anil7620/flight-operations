
from flask import render_template, request, redirect, url_for, session, flash
from flight import flight 
import logging
from datetime import datetime, timedelta
from bson.objectid import ObjectId 
from flask import jsonify 
from flight.model.admin import Admin
from flight.model.customer import Customer 
from flight.model.airport import Airport



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
        
@flight.route('/admin_airports', methods=['GET', 'POST'])
def admin_airports():
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        airport_name = request.form.get("airport_name").strip()
        city = request.form.get("city").strip()
        state = request.form.get("state").strip()
        zipcode = request.form.get("zipcode").strip()
        phone = request.form.get("phone").strip()
        email = request.form.get("email").strip()
        data = {
            "airport_name": airport_name,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "phone": phone,
            "email": email
        }
        Airport.create(data)
        flash("Airport added successfully!", "success")
        return redirect(url_for('admin_airports'))
    
    airports = Airport.get_all()
    return render_template('admin/admin_manage_airports.html', airports=airports)


# edit
@flight.route('/admin_airports/<airport_id>', methods=['GET', 'POST'])
def admin_airport_edit(airport_id):
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        airport_name = request.form.get("airport_name").strip()
        city = request.form.get("city").strip()
        state = request.form.get("state").strip()
        zipcode = request.form.get("zipcode").strip()
        phone = request.form.get("phone").strip()
        email = request.form.get("email").strip()
        data = {
            "airport_name": airport_name,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "phone": phone,
            "email": email
        }
        Airport.update(ObjectId(airport_id), data)
        flash("Airport updated successfully!", "success")
        return redirect(url_for('admin_airports'))
    
    airport = Airport.get_by_id(ObjectId(airport_id))
    return render_template('admin/admin_edit_airport.html', airport=airport)


@flight.route('/admin_airports/delete/<airport_id>', methods=['GET'])
def admin_airport_delete(airport_id):
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    
    Airport.delete(ObjectId(airport_id))
    flash("Airport deleted successfully!", "success")
    return redirect(url_for('admin_airports'))

