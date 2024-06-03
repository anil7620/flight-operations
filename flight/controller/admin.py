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

@flight.route('/admin_signup', methods=['GET'])
def admin_signup():
    try:
        # Hard-coded admin data
        email = "admin@admin.com"
        user_name = "Admin User"
        phone = "123-456-7890"
        password = "123"

        # Check if the admin email is already registered
        if Admin.exists_by_email(email):
            flash({"message": "Admin already registered. Check DB for details."}), 200
            return redirect(url_for('admin_login'))

        # Data preparation
        data = {
            "user_name": user_name,
            "email": email,
            "phone": phone,
            "password": password
        }

        # Create admin record
        Admin.create(data)
        flash({"message": "Admin registered successfully!"}), 201
        return redirect(url_for('admin_login'))

    except Exception as e:
        logger.error(f"Error during admin registration: {str(e)}")
        return "Internal Server Error", 500



@flight.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        
        # Check if user exists in the admin database
        if Admin.exists_by_email(email):
            admin = Admin.get_by_email(email)
            if (admin['password'], password):
                session["user_id"] = str(admin['_id'])
                session["user_type"] = "admin"
                return redirect(url_for('admin_dashboard'))
            else:
                return "Invalid credentials", 400
        else:
            return "No such admin", 404

    return render_template('admin/login.html')


@flight.route('/admin_dashboard')
def admin_dashboard():
    if session["user_type"] != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('admin_login')) 
    return render_template('admin/home.html')


@flight.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))



