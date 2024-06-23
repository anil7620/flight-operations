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
            return redirect(url_for('login'))

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
        return redirect(url_for('login'))

    except Exception as e:
        logger.error(f"Error during admin registration: {str(e)}")
        return "Internal Server Error", 500



@flight.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next') or url_for('dashboard')
    
    if request.method == 'POST':
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        user_type = request.form.get("user_type").strip()

        print(f"Next URL: {next_url}")

        if user_type == "admin":
            # Admin login logic
            if Admin.exists_by_email(email):
                admin = Admin.get_by_email(email)
                if admin['password'] == password:
                    session["user_id"] = str(admin['_id']) 
                    session["user_type"] = "admin"
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash("Invalid credentials", "error")
                    return redirect(url_for('login', next=next_url))
            else:
                flash("No such admin", "error")
                return redirect(url_for('login', next=next_url))
        elif user_type == "customer":
            # Customer login logic
            if Customer.exists_by_email(email):
                customer = Customer.get_by_email(email)
                if customer['password'] == password:
                    session["user_id"] = str(customer['_id']) 
                    session["user_type"] = "customer"
                    return redirect(url_for('customer_dashboard'))
                else:
                    flash("Invalid credentials", "error")
                    return redirect(url_for('login', next=next_url))
            else:
                flash("No such customer", "error")
                return redirect(url_for('login', next=next_url))
        else:
            flash("Invalid user type", "error")
            return redirect(url_for('login', next=next_url))
    
    return render_template('login.html', next=next_url)


@flight.route('/dashboard')
def dashboard():
    if session.get("user_type") == "admin":
        return redirect(url_for('admin_dashboard'))
    elif session.get("user_type") == "customer":
        return redirect(url_for('customer_dashboard'))
    else:
        flash("Unauthorized access.", "error")
        return redirect(url_for('login')) 


@flight.route('/admin_dashboard')
def admin_dashboard():
    if session.get("user_type") != "admin":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login')) 
    return render_template('admin/home.html')


@flight.route('/customer_dashboard')
def customer_dashboard():
    if session.get("user_type") != "customer":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login')) 
    return render_template('customer/home.html', is_logged_in=True)


@flight.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



