from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_utils import getCursor

auth_bp = Blueprint('auth', __name__)

# modules/auth.py

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('user.dashboard'))

    email = ""
    password = ""

    if request.method == 'POST':
        email, password = request.form.get('email'), request.form.get('password')
        cur = getCursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s AND role='user'", (email, password))
        user = cur.fetchone()
        
        if user:
            session.update({'user_id': user['id'], 'user_name': user['name'], 'role': 'user'})
            return redirect(url_for('user.dashboard'))
        
        # If login fails:
        flash("Invalid Credentials. Please check your email and password.", "danger")
        return render_template('auth/login.html', email=email, password=password)

    return render_template('auth/login.html', email=email, password=password)

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    email = ""
    password = ""

    if request.method == 'POST':
        email, password = request.form.get('email'), request.form.get('password')
        cur = getCursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s AND role='admin'", (email, password))
        admin = cur.fetchone()
        
        if admin:
            session.clear() 
            session.update({
                'user_id': admin['id'],
                'user_name': admin['name'],
                'role': 'admin'
            })
            return redirect(url_for('admin.dashboard')) 
        
        # If login fails:
        flash("Unauthorized Admin Access. Access Denied.", "danger")
        return render_template('admin/login.html', email=email, password=password)

    return render_template('admin/login.html', email=email, password=password)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = (request.form.get('name'), request.form.get('email'), request.form.get('phone'), request.form.get('password'))
        cur = getCursor()
        try:
            cur.execute("INSERT INTO users (name, email, phone, password, role) VALUES (%s,%s,%s,%s, 'user')", data)
            flash("Account created! Login now.", "success")
            return redirect(url_for('auth.login'))
        except: flash("Email exists", "danger")
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))