from flask import render_template, request, redirect, url_for, session, flash
from flight import flight 
import logging
from datetime import datetime
from bson.objectid import ObjectId 
from flask import jsonify 
from flight.model.customer import Customer 
from flight.model.reservation import Reservation
from flight.model.airport import Airport
from flight.model.flight import Flight

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@flight.route('/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        try:
            # Data from form
            firstname = request.form.get("firstname").strip()
            lastname = request.form.get("lastname").strip()
            email = request.form.get("email").strip()
            password = request.form.get("password").strip()
            confirm_password = request.form.get("confirm_password").strip()
            dob = request.form.get("dob").strip()
            city = request.form.get("city").strip()
            state = request.form.get("state").strip()
            zipcode = request.form.get("zipcode").strip()

            # Check if passwords match
            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for('customer_signup'))

            # Check if the customer email is already registered
            if Customer.exists_by_email(email):
                flash("Customer already registered.", "error")
                return redirect(url_for('login'))

            # Data preparation
            data = {
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "password": password,
                "dob": dob,
                "city": city,
                "state": state,
                "zipcode": zipcode
            }

            # Create customer record
            Customer.create(data)
            flash("Customer registered successfully!", "success")
            return redirect(url_for('login'))

        except Exception as e:
            logger.error(f"Error during customer registration: {str(e)}")
            return "Internal Server Error", 500

    return render_template('customer/signup.html')



# @flight.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get("email").strip()
#         password = request.form.get("password").strip()
        
#         # Check if user exists in the customer database
#         if Customer.exists_by_email(email):
#             customer = Customer.get_by_email(email)
#             if customer['password'] == password:
#                 session["user_id"] = str(customer['_id']) 
#                 session["user_type"] = "customer"
#                 next_url = request.form.get('next')
#                 return redirect(next_url or url_for('customer_dashboard'))
#             else:
#                 flash("Invalid credentials", "error")
#                 return redirect(url_for('login'))
#         else:
#             flash("No such customer", "error")
#             return redirect(url_for('login'))
#     next_url = request.args.get('next')
#     return render_template('customer/login.html', next=next_url)

# @flight.route('/login', methods=['GET', 'POST'])
# def login():
#     next_url = request.args.get('next') or request.form.get('next') or url_for('customer_dashboard')

#     if request.method == 'POST':
#         email = request.form.get("email").strip()
#         password = request.form.get("password").strip()

#         print(f"Next URL: {next_url}")

#         # Check if user exists in the customer database
#         if Customer.exists_by_email(email):
#             customer = Customer.get_by_email(email)
#             if customer['password'] == password:
#                 session["user_id"] = str(customer['_id']) 
#                 session["user_type"] = "customer"
#                 return redirect(next_url)
#             else:
#                 flash("Invalid credentials", "error")
#                 return redirect(url_for('login', next=next_url))
#         else:
#             flash("No such customer", "error")
#             return redirect(url_for('login', next=next_url))

#     return render_template('customer/login.html', next=next_url)


# @flight.route('/customer_dashboard')
# def customer_dashboard():
#     if session.get("user_type") != "customer":
#         flash("Unauthorized access.", "error")
#         return redirect(url_for('login')) 
#     return render_template('customer/home.html', is_logged_in=True)








# @flight.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))



@flight.route('/customer_bookings')
def customer_bookings():
    if session.get("user_type") != "customer":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    
    customer_id = session.get("user_id")
    bookings = Reservation.get_bookings(customer_id)

    for booking in bookings: 
        flight = Flight.get_by_id(ObjectId(booking['flight_id']))
        if flight:
            origin_airport = Airport.get_by_id(flight['origin_airport'])
            destination_airport = Airport.get_by_id(flight['destination_airport'])
            booking['flight'] = flight
            booking['flight']['origin_airport_name'] = origin_airport['airport_name'] if origin_airport else "Unknown"
            booking['flight']['destination_airport_name'] = destination_airport['airport_name'] if destination_airport else "Unknown"
    
    return render_template('customer/bookings.html', bookings=bookings)
    
    print(bookings)
    return render_template('customer/bookings.html', bookings=bookings)

# cancel_reservation/665c248690cba958e3c4c85b
@flight.route('/cancel_reservation/<reservation_id>')
def cancel_reservation(reservation_id):
    if session.get("user_type") != "customer":
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    
    try:
        reservation = Reservation.get_by_id(ObjectId(reservation_id))
        if reservation and reservation['user_id'] == session.get("user_id"):
            Reservation.delete(ObjectId(reservation_id))
            flash("Reservation cancelled successfully.")
        else:
            flash("Reservation not found.")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
    return redirect(url_for('customer_bookings'))

