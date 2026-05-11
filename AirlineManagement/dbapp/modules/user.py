from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
from db_utils import getCursor
from modules.pdf_service import generate_boarding_pass_pdf
import uuid, io
from datetime import datetime, date # Added date for age calculation

user_bp = Blueprint('user', __name__)

# --- Added Age Calculation Helper ---
def calculate_age(birth_date_str):
    if not birth_date_str:
        return 0
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

@user_bp.route('/search')
def search():
    src = request.args.get('source')
    dst = request.args.get('dest')
    date_val = request.args.get('travel_date')
    
    if not src or not dst or not date_val:
        return redirect(url_for('index'))

    cur = getCursor()
    cur.execute("""
        SELECT f.id, f.airline, f.flight_num, f.dep_time, f.arr_time, f.base_price, f.discount_pct,
               a1.city as src_name, a2.city as dst_name 
        FROM flights f
        JOIN airports a1 ON f.dep_code = a1.code 
        JOIN airports a2 ON f.arr_code = a2.code
        WHERE f.dep_code=%s AND f.arr_code=%s AND DATE(f.dep_time)=%s
    """, (src, dst, date_val))
    
    flights = cur.fetchall()
    
    for f in flights:
        f['final_price'] = float(f['base_price']) * (1 - (int(f['discount_pct'])/100))
        
    return render_template('user/results.html', flights=flights, src=src, dst=dst, date=date_val)

@user_bp.route('/book/<int:flight_id>')
def book_step1(flight_id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    cur = getCursor()
    cur.execute("SELECT f.*, a1.city as src, a2.city as dst FROM flights f JOIN airports a1 ON f.dep_code=a1.code JOIN airports a2 ON f.arr_code=a2.code WHERE f.id=%s", (flight_id,))
    return render_template('user/booking_details.html', flight=cur.fetchone())

@user_bp.route('/book_seats', methods=['POST'])
def book_step2():
    # --- Updated to handle Age Calculation ---
    passenger_data = request.form.to_dict()
    # Calculate age from DOB before storing in session
    passenger_data['passenger_age'] = calculate_age(request.form.get('dob'))
    session['booking_data'] = passenger_data
    
    cur = getCursor()
    cur.execute("SELECT * FROM flights WHERE id=%s", (request.form.get('flight_id'),))
    flight = cur.fetchone()
    flight['final_base_price'] = float(flight['base_price']) * (1 - (int(flight['discount_pct'])/100))
    return render_template('user/booking_seats.html', flight=flight)

@user_bp.route('/payment', methods=['POST'])
def payment():
    data = session.get('booking_data')
    if not data:
        return redirect(url_for('index'))
    data.update({
        'seat_num': request.form.get('seat_num'),
        'class_type': request.form.get('class_type')
    })
    raw_price = float(request.form.get('total_price'))
    tax = raw_price * 0.18
    conv_fee = 250.00
    total = raw_price + tax + conv_fee
    session.update({
        'booking_data': data,
        'final_payable_amount': total
    })
    cur = getCursor()
    cur.execute("""
        SELECT f.*, a1.city as src, a2.city as dst 
        FROM flights f 
        JOIN airports a1 ON f.dep_code = a1.code 
        JOIN airports a2 ON f.arr_code = a2.code 
        WHERE f.id = %s
    """, (data['flight_id'],))
    flight = cur.fetchone()
    discount_pct = int(flight['discount_pct'])
    discount_amount = 0
    if discount_pct > 0:
        original_price = raw_price / (1 - (discount_pct / 100))
        discount_amount = original_price - raw_price
    return render_template('user/payment.html', 
                           data=data, 
                           flight=flight, 
                           total_amount=total, 
                           base_price=raw_price, 
                           tax=tax,
                           discount_amount=discount_amount)

@user_bp.route('/process_final_payment', methods=['POST'])
def process_final():
    d = session.get('booking_data')
    amt = session.get('final_payable_amount')
    uid = session.get('user_id')
    
    cur = getCursor()
    # --- Updated INSERT query to include all new details for Admin monitoring ---
    cur.execute("""
        INSERT INTO bookings (
            user_id, flight_id, passenger_name, passenger_age, passenger_gender, 
            seat_num, class, total_paid, gov_id, nationality, dob, 
            phone_num, medical_info, infant_details
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        uid, d['flight_id'], d['passenger_name'], d['passenger_age'], d['passenger_gender'],
        d['seat_num'], d['class_type'], amt, d['gov_id'], d['nationality'], d['dob'],
        d['phone_num'], d.get('medical_info', ''), d.get('infant_details', '')
    ))
    
    b_id = cur.lastrowid
    cur.execute("INSERT INTO payments (booking_id, transaction_id, amount_paid) VALUES (%s,%s,%s)", 
                (b_id, f"BA-{uuid.uuid4().hex[:6].upper()}", amt))
    
    # Success, clear the session data
    session.pop('booking_data', None)
    return redirect(url_for('user.success', b_id=b_id))

@user_bp.route('/success/<int:b_id>')
def success(b_id): return render_template('user/payment_success.html', b_id=b_id)

@user_bp.route('/download_ticket/<int:b_id>')
def download_ticket(b_id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    cur = getCursor()
    cur.execute("""
        SELECT b.*, f.flight_num, f.airline, f.dep_time, f.arr_time,
               a1.city as src, a1.code as src_code, a1.name as src_name,
               a2.city as dst, a2.code as dst_code, a2.name as dst_name
        FROM bookings b 
        JOIN flights f ON b.flight_id = f.id
        JOIN airports a1 ON f.dep_code = a1.code 
        JOIN airports a2 ON f.arr_code = a2.code
        WHERE b.id = %s AND b.user_id = %s
    """, (b_id, session['user_id']))
    t = cur.fetchone()
    if not t:
        flash("Ticket not found.", "danger")
        return redirect(url_for('user.dashboard'))
    try:
        pdf_bytes = generate_boarding_pass_pdf(t)
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=f"BoundlessAir_BoardingPass_{t['flight_num']}.pdf")
    except Exception as e:
        flash("Error generating PDF.", "danger")
        return redirect(url_for('user.dashboard'))

@user_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    cur = getCursor()
    cur.execute("SELECT * FROM airports ORDER BY state, city")
    airports_list = cur.fetchall()
    cur.execute("""
        SELECT b.*, f.flight_num, f.airline, f.dep_time, a1.city as src, a2.city as dst
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        JOIN airports a1 ON f.dep_code = a1.code
        JOIN airports a2 ON f.arr_code = a2.code
        WHERE b.user_id = %s
        ORDER BY b.booking_date DESC
    """, (session['user_id'],))
    my_bookings = cur.fetchall()
    return render_template('user/dashboard.html', airports=airports_list, bookings=my_bookings)