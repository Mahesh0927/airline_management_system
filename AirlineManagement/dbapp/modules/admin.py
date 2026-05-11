from flask import Blueprint, render_template, session, redirect, url_for, request, flash,  jsonify, send_file
from modules.pdf_service import generate_boarding_pass_pdf
from db_utils import getCursor
from datetime import date
import io;

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def dashboard():
    if session.get('role') != 'admin': 
        return redirect(url_for('auth.admin_login'))
    
    cur = getCursor()
    
    # 1. Metrics with simulated trends
    cur.execute("SELECT COUNT(*) as total FROM bookings")
    total_bookings = cur.fetchone()['total']
    
    cur.execute("SELECT COALESCE(SUM(total_paid), 0) as total FROM bookings WHERE status='Confirmed'")
    total_revenue = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM flights WHERE dep_time > NOW()")
    active_flights = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM users WHERE role='user'")
    total_users = cur.fetchone()['total']

    # 2. Exclusive Route Data (Top 5)
    cur.execute("""
        SELECT 
            CONCAT(a1.code, ' → ', a2.code) as route, 
            COUNT(b.id) as total_bookings 
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        JOIN airports a1 ON f.dep_code = a1.code
        JOIN airports a2 ON f.arr_code = a2.code
        GROUP BY route
        ORDER BY total_bookings DESC
        LIMIT 5
    """)
    route_data = cur.fetchall()
    
    # 3. Recent Bookings
    cur.execute("""
        SELECT b.passenger_name, b.total_paid, b.status, f.flight_num, f.airline, b.booking_date 
        FROM bookings b 
        JOIN flights f ON b.flight_id = f.id 
        ORDER BY b.booking_date DESC LIMIT 10
    """)
    recent_bookings = cur.fetchall()

    return render_template('admin/dashboard.html', 
                           metrics={'bookings': total_bookings, 'revenue': total_revenue, 'flights': active_flights, 'users': total_users},
                           route_data=route_data,
                           recent_bookings=recent_bookings)

# ================= FLIGHT MANAGEMENT =================
@admin_bp.route('/admin/flights',methods=['GET'])
def manage_flights():
    if session.get('role') != 'admin': return redirect(url_for('auth.admin_login'))
    
     # 1. Get filter date from request or default to today
    filter_date = request.args.get('filter_date')
    filter_time = request.args.get('filter_time')
    if not filter_date:
        filter_date = date.today().strftime('%Y-%m-%d')
    if not filter_time:
        filter_time = "00:00"

    cur = getCursor()
    # Fetch all flights with detailed route info and total bookings count
    query = """
        SELECT f.*, 
               a1.city as src, a1.code as src_code,
               a2.city as dst, a2.code as dst_code,
               COUNT(b.id) as booked_count
        FROM flights f
        JOIN airports a1 ON f.dep_code = a1.code
        JOIN airports a2 ON f.arr_code = a2.code
        LEFT JOIN bookings b ON f.id = b.flight_id
        WHERE DATE(f.dep_time) = %s AND TIME(f.dep_time) >= %s
        GROUP BY f.id
        ORDER BY f.dep_time ASC
        LIMIT 10
    """
    cur.execute(query, (filter_date,filter_time))
    flights = cur.fetchall()
    
    # Fetch airports for the dropdowns
    cur.execute("SELECT code, city FROM airports ORDER BY city")
    airports = cur.fetchall()
    
    return render_template('admin/flights.html', flights=flights, airports=airports, selected_date=filter_date,selected_time=filter_time)

from datetime import datetime

@admin_bp.route('/admin/flights/add', methods=['POST'])
def add_flight():
    if session.get('role') != 'admin': 
        return redirect(url_for('auth.admin_login'))
    
    # 1. Collect Form Data
    airline = request.form.get('airline')
    flight_num = request.form.get('flight_num').strip().upper()
    dep_code = request.form.get('dep')
    arr_code = request.form.get('arr')
    dep_time_str = request.form.get('dep_t')
    arr_time_str = request.form.get('arr_t')
    price = request.form.get('price')
    discount = request.form.get('disc')

    # --- SERVER SIDE VALIDATION ---
    
    # A. Check for empty fields
    if not all([airline, flight_num, dep_code, arr_code, dep_time_str, arr_time_str, price]):
        flash("All fields are required to initialize a flight.", "danger")
        return redirect(url_for('admin.manage_flights'))

    # B. Logical Check: Route
    if dep_code == arr_code:
        flash("Validation Error: Departure and Arrival cities cannot be the same.", "warning")
        return redirect(url_for('admin.manage_flights'))

    # C. Datetime Parsing and Logic
    try:
        dep_dt = datetime.strptime(dep_time_str, '%Y-%m-%dT%H:%M')
        arr_dt = datetime.strptime(arr_time_str, '%Y-%m-%dT%H:%M')
        now = datetime.now()

        if dep_dt < now:
            flash("Validation Error: Departure time cannot be in the past.", "warning")
            return redirect(url_for('admin.manage_flights'))

        if arr_dt <= dep_dt:
            flash("Validation Error: Arrival time must be after Departure time.", "warning")
            return redirect(url_for('admin.manage_flights'))
    except ValueError:
        flash("Invalid date format provided.", "danger")
        return redirect(url_for('admin.manage_flights'))

    # D. Numeric Validation
    try:
        price_val = float(price)
        disc_val = int(discount) if discount else 0
        if price_val <= 0:
            flash("Price must be a positive amount.", "warning")
            return redirect(url_for('admin.manage_flights'))
        if disc_val < 0 or disc_val > 100:
            flash("Discount must be between 0 and 100.", "warning")
            return redirect(url_for('admin.manage_flights'))
    except ValueError:
        flash("Price and Discount must be valid numbers.", "danger")
        return redirect(url_for('admin.manage_flights'))

    # 2. Database Insertion
    cur = getCursor()
    try:
        cur.execute("""
            INSERT INTO flights (airline, flight_num, dep_code, arr_code, dep_time, arr_time, base_price, discount_pct, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Scheduled')
        """, (airline, flight_num, dep_code, arr_code, dep_dt, arr_dt, price_val, disc_val))
        
        flash(f"Success: Flight {flight_num} has been initialized in the system.", "success")
    except Exception as e:
        # Catch SQL unique constraint errors (if flight_num exists)
        flash("Database Error: Could not save flight. Ensure Flight Number is unique.", "danger")
        print(f"SQL Error: {e}")

    return redirect(url_for('admin.manage_flights'))

@admin_bp.route('/admin/flights/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    fid = data.get('flight_id')
    new_status = data.get('status')
    cur = getCursor()
    cur.execute("UPDATE flights SET status=%s WHERE id=%s", (new_status, fid))
    return jsonify({"success": True, "message": f"Flight {fid} is now {new_status}"})

@admin_bp.route('/admin/flights/delete/<int:fid>')
def delete_flight(fid):
    cur = getCursor()
    # Check if bookings exist before deleting
    cur.execute("SELECT COUNT(*) as count FROM bookings WHERE flight_id=%s", (fid,))
    if cur.fetchone()['count'] > 0:
        flash("Cannot delete flight with active bookings. Cancel bookings first.", "warning")
    else:
        cur.execute("DELETE FROM flights WHERE id=%s", (fid,))
        flash("Flight removed successfully.", "info")
    return redirect(url_for('admin.manage_flights'))

# ================= BOOOKINGS MONITOR =================

@admin_bp.route('/admin/bookings', methods=['GET'])
def manage_bookings():
    if session.get('role') != 'admin': return redirect(url_for('auth.admin_login'))
    
    cur = getCursor()
    
    # 1. Get filter parameters
    search_query = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '')

    # 2. Base Query with Joins to get full details
    query = """
        SELECT b.*, f.flight_num, f.airline, f.dep_time,
               a1.city as src, a2.city as dst, u.email as user_email
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        JOIN airports a1 ON f.dep_code = a1.code
        JOIN airports a2 ON f.arr_code = a2.code
        JOIN users u ON b.user_id = u.id
        WHERE 1=1
    """
    params = []

    if search_query:
        query += " AND (b.passenger_name LIKE %s OR b.gov_id LIKE %s OR f.flight_num LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
    
    if status_filter:
        query += " AND b.status = %s"
        params.append(status_filter)

    query += " ORDER BY b.booking_date DESC LIMIT 100"
    
    cur.execute(query, tuple(params))
    bookings = cur.fetchall()

    # 3. Get counts for the summary cards
    cur.execute("SELECT status, COUNT(*) as count FROM bookings GROUP BY status")
    status_counts = {row['status']: row['count'] for row in cur.fetchall()}

    return render_template('admin/bookings.html', 
                           bookings=bookings, 
                           counts=status_counts,
                           search=search_query,
                           selected_status=status_filter)

@admin_bp.route('/admin/booking/update_status', methods=['POST'])
def update_booking_status():
    if session.get('role') != 'admin': return jsonify({"success": False}), 403
    
    data = request.get_json()
    bid = data.get('booking_id')
    new_status = data.get('status')
    
    cur = getCursor()
    cur.execute("UPDATE bookings SET status=%s WHERE id=%s", (new_status, bid))
    return jsonify({"success": True, "message": "Booking status updated."})

# --- 1. JSON API for the 'Eye' Button ---
@admin_bp.route('/admin/booking/details/<int:bid>')
def booking_details_api(bid):
    if session.get('role') != 'admin': 
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    try:
        cur = getCursor()
        # Explicitly select columns to avoid ambiguity
        cur.execute("""
            SELECT b.passenger_name, b.passenger_age, b.passenger_gender, 
                   b.gov_id, b.nationality, b.phone_num, b.medical_info,
                   b.seat_num, b.class, b.total_paid, b.status,
                   f.flight_num, f.airline, f.dep_time, f.arr_time,
                   a1.city as src, a2.city as dst,
                   u.name as account_holder, u.email as account_email
            FROM bookings b
            JOIN flights f ON b.flight_id = f.id
            JOIN airports a1 ON f.dep_code = a1.code
            JOIN airports a2 ON f.arr_code = a2.code
            JOIN users u ON b.user_id = u.id
            WHERE b.id = %s
        """, (bid,))
        details = cur.fetchone()
        
        if not details:
            return jsonify({"success": False, "message": "Booking record not found in database."})

        # Safe formatting for dates (handles cases where dates might be missing)
        if details['dep_time']:
            details['dep_time'] = details['dep_time'].strftime('%d %b %Y, %H:%M')
        if details['arr_time']:
            details['arr_time'] = details['arr_time'].strftime('%d %b %Y, %H:%M')

        # Ensure total_paid is a string for JSON
        details['total_paid'] = str(details['total_paid'])

        return jsonify({"success": True, "data": details})

    except Exception as e:
        # This will print the EXACT error in your Python terminal (VS Code / CMD)
        print(f"CRITICAL ERROR in booking_details_api: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# --- 2. Admin Download Route (Bypasses User-ID check) ---
@admin_bp.route('/admin/booking/download/<int:bid>')
def admin_download_ticket(bid):
    if session.get('role') != 'admin': return redirect(url_for('auth.admin_login'))
    
    cur = getCursor()
    cur.execute("""
        SELECT b.*, f.flight_num, f.airline, f.dep_time, f.arr_time,
               a1.city as src, a1.code as src_code, a2.city as dst, a2.code as dst_code
        FROM bookings b 
        JOIN flights f ON b.flight_id = f.id
        JOIN airports a1 ON f.dep_code = a1.code 
        JOIN airports a2 ON f.arr_code = a2.code
        WHERE b.id = %s
    """, (bid,))
    t = cur.fetchone()

    if not t: return "Ticket not found"

    pdf_bytes = generate_boarding_pass_pdf(t)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Admin_Copy_{t['flight_num']}_{t['passenger_name']}.pdf"
    )

# ================= USER MANAGEMENT =================
@admin_bp.route('/admin/users')
def manage_users():
    if session.get('role') != 'admin': return redirect(url_for('auth.admin_login'))
    
    search_query = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '')

    cur = getCursor()
    
    # Base query to fetch users and their total contribution to Boundless Air
    query = """
        SELECT u.*, 
               COUNT(b.id) as total_bookings, 
               COALESCE(SUM(b.total_paid), 0) as total_spent
        FROM users u
        LEFT JOIN bookings b ON u.id = b.user_id
        WHERE u.role = 'user'
    """
    params = []

    if search_query:
        query += " AND (u.name LIKE %s OR u.email LIKE %s OR u.phone LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
    
    if status_filter:
        val = 1 if status_filter == 'Blocked' else 0
        query += " AND u.is_blocked = %s"
        params.append(val)

    query += " GROUP BY u.id ORDER BY total_spent DESC"
    
    cur.execute(query, tuple(params))
    users = cur.fetchall()

    # Metrics for Top Summary Cards
    cur.execute("SELECT COUNT(*) as total FROM users WHERE role='user'")
    total_count = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM users WHERE role='user' AND is_blocked=1")
    blocked_count = cur.fetchone()['total']

    return render_template('admin/users.html', 
                           users=users, 
                           total_count=total_count, 
                           blocked_count=blocked_count,
                           search=search_query)

# --- AJAX: Toggle Block Status ---
@admin_bp.route('/admin/users/toggle/<int:uid>', methods=['POST'])
def toggle_user_block(uid):
    if session.get('role') != 'admin': return jsonify({"success": False}), 403
    cur = getCursor()
    cur.execute("UPDATE users SET is_blocked = NOT is_blocked WHERE id=%s", (uid,))
    return jsonify({"success": True})

# --- AJAX: User History Deep-Dive ---
@admin_bp.route('/admin/users/history/<int:uid>')
def user_history_api(uid):
    if session.get('role') != 'admin': return jsonify({"success": False}), 403
    cur = getCursor()
    cur.execute("""
        SELECT b.id, b.passenger_name, b.total_paid, b.status, f.flight_num, 
               a1.city as src, a2.city as dst, b.booking_date
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        JOIN airports a1 ON f.dep_code = a1.code
        JOIN airports a2 ON f.arr_code = a2.code
        WHERE b.user_id = %s
        ORDER BY b.booking_date DESC
    """, (uid,))
    history = cur.fetchall()
    
    for h in history:
        h['booking_date'] = h['booking_date'].strftime('%d %b %Y')
        h['total_paid'] = "{:,.2f}".format(float(h['total_paid']))

    return jsonify({"success": True, "history": history})

# ================= OFFER MANAGEMENT =================

# --- VIEW ALL OFFERS ---
@admin_bp.route('/admin/offers')
def manage_offers():
    if session.get('role') != 'admin': return redirect(url_for('auth.admin_login'))
    
    cur = getCursor()
    # Auto-update status to 'Expired' if date has passed
    cur.execute("UPDATE promos SET status='Expired' WHERE expiry_date < CURDATE()")
    
    cur.execute("SELECT * FROM promos ORDER BY created_at DESC")
    promos = cur.fetchall()
    
    return render_template('admin/offers.html', promos=promos)

# --- ADD NEW PROMO ---
@admin_bp.route('/admin/offers/add', methods=['POST'])
def add_offer():
    if session.get('role') != 'admin': return redirect(url_for('auth.admin_login'))
    
    code = request.form.get('code').strip().upper()
    discount = request.form.get('discount')
    expiry = request.form.get('expiry')
    
    # Validation
    if not code or not discount or not expiry:
        flash("All fields are required.", "danger")
        return redirect(url_for('admin.manage_offers'))
    
    try:
        cur = getCursor()
        cur.execute("INSERT INTO promos (code, discount_pct, expiry_date) VALUES (%s, %s, %s)", 
                    (code, discount, expiry))
        flash(f"Promo code {code} is now live!", "success")
    except:
        flash("Error: Code already exists.", "danger")
        
    return redirect(url_for('admin.manage_offers'))

# --- DELETE OFFER ---
@admin_bp.route('/admin/offers/delete/<int:oid>')
def delete_offer(oid):
    if session.get('role') != 'admin': return redirect(url_for('auth.admin_login'))
    cur = getCursor()
    cur.execute("DELETE FROM promos WHERE id=%s", (oid,))
    flash("Offer removed from system.", "info")
    return redirect(url_for('admin.manage_offers'))