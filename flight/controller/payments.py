from flask import request, redirect, url_for, render_template, session, flash
from flight import flight
from flight.model.reservation import Reservation
from flight.model.payments import Payment
from flight.model.airplane import Airplane
from flight.model.flight import Flight
from bson.objectid import ObjectId
from datetime import datetime

# @flight.route('/book/<flight_id>/<seat_type>', methods=['GET', 'POST'])
# def book_seat(flight_id, seat_type):
#     if 'user_id' not in session:
#         return redirect(url_for('customer_login', next=url_for('book_seat', flight_id=flight_id, seat_type=seat_type)))

#     flight = Flight.get_by_id(ObjectId(flight_id))
#     if not flight:
#         flash("Flight not found.")
#         return redirect(url_for('home'))

#     if request.method == 'POST':
#         try:
#             # Get form data
#             num_passengers = int(request.form.get("num_passengers"))
#             passengers = []
#             for i in range(1, num_passengers + 1):
#                 passenger = {
#                     "name": request.form.get(f"passenger_{i}_name"),
#                     "age": request.form.get(f"passenger_{i}_age")
#                 }
#                 passengers.append(passenger)

#             card_name = request.form.get("card_name")
#             card_number = request.form.get("card_number")
#             card_expiry = request.form.get("card_expiry")
#             card_cvc = request.form.get("card_cvc")

#             # Save reservation details
#             reservation_data = {
#                 "user_id": session["user_id"],
#                 "flight_id": flight_id,
#                 "seat_type": seat_type,
#                 "num_passengers": num_passengers,
#                 "passengers": passengers,
#                 "date_reserved": datetime.now()
#             }
#             Reservation.create(reservation_data)

#             # Save payment details
#             payment_data = {
#                 "user_id": session["user_id"],
#                 "card_name": card_name,
#                 "card_number": card_number,
#                 "card_expiry": card_expiry,
#                 "card_cvc": card_cvc,
#                 "amount": flight['seats_cost'][seat_type] * num_passengers,
#                 "date_paid": datetime.now()
#             }
#             payment = Payment.create(payment_data)

#             # get payment id
#             payment_id = payment.inserted_id
#             print("done payment info")

#             # update to resewrvation
#             Reservation.update_payment_id(payment_id, reservation_data)
#             print("done updating reservation")

#             # Update seat count in the airplane
#             flight_id = flight["flight_id"]
#             print("reached in controller 1")
#             Flight.update_seat_count(flight_id, seat_type, num_passengers)
#             print("reached in controller 2")

#             flash("Booking confirmed successfully!", "success")
#             return redirect(url_for('customer_dashboard'))
#         except Exception as e:
#             flash(f"An error occurred: {str(e)}", "error")
#             return redirect(url_for('book_seat', flight_id=flight_id, seat_type=seat_type))

#     return render_template('customer/confirm_booking.html', flight=flight, seat_type=seat_type, seat_cost=flight['seats_cost'][seat_type])


@flight.route('/book/<flight_id>/<seat_type>', methods=['GET', 'POST'])
def book_seat(flight_id, seat_type):
    if 'user_id' not in session:
        return redirect(url_for('customer_login', next=url_for('book_seat', flight_id=flight_id, seat_type=seat_type)))

    flight = Flight.get_by_id(ObjectId(flight_id))
    if not flight:
        flash("Flight not found.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        try:
            # Get form data
            num_passengers = int(request.form.get("num_passengers"))
            passengers = []
            for i in range(1, num_passengers + 1):
                passenger = {
                    "name": request.form.get(f"passenger_{i}_name"),
                    "age": request.form.get(f"passenger_{i}_age")
                }
                passengers.append(passenger)

            card_name = request.form.get("card_name")
            card_number = request.form.get("card_number")
            card_expiry = request.form.get("card_expiry")
            card_cvc = request.form.get("card_cvc")

            # Save reservation details
            reservation_data = {
                "user_id": session["user_id"],
                "flight_id": flight_id,
                "seat_type": seat_type,
                "num_passengers": num_passengers,
                "passengers": passengers,
                "status": "confirm", 
                "date_reserved": datetime.now()
            }
            reservation = Reservation.create(reservation_data)

            # Save payment details
            payment_data = {
                "user_id": session["user_id"],
                "card_name": card_name,
                "card_number": card_number,
                "card_expiry": card_expiry,
                "card_cvc": card_cvc,
                "status": "paid",
                "amount": flight['seats_cost'][seat_type] * num_passengers,
                "date_paid": datetime.now()
            }
            payment = Payment.create(payment_data)

            # Update reservation with payment ID
            payment_id = payment.inserted_id
            Reservation.update_payment_id(reservation.inserted_id, payment_id)

            # Update seat count in the flight
            Flight.update_seat_count(flight_id, seat_type, num_passengers)

            flash("Booking confirmed successfully!", "success")
            return redirect(url_for('customer_dashboard'))
        except Exception as e:
            print(e)
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('book_seat', flight_id=flight_id, seat_type=seat_type))

    return render_template('customer/confirm_booking.html', flight=flight, seat_type=seat_type, seat_cost=flight['seats_cost'][seat_type])
