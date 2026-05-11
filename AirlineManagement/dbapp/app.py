from flask import Flask, render_template,Blueprint,request,redirect,url_for,session, g
from db_utils import getCursor
from modules.auth import auth_bp
from modules.user import user_bp
from modules.admin import admin_bp
from modules.chatbot import chatbot_bp

app = Flask(__name__)
app.secret_key = "boundless_air_premium_key"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(chatbot_bp)

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None: db.close()

@app.route('/')
def index():
    #If user is already logged in, send them to dashboard
    if 'user_id' in session:
        if session.get('role') == 'user':
            return redirect(url_for('user.dashboard'))
        elif session.get('role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        
    # If no session, show the normal landing page    
    cur = getCursor()
    cur.execute("SELECT * FROM airports ORDER BY state, city")
    return render_template('index.html', airports=cur.fetchall())

@app.route('/airlines')
def airlines(): return render_template('airlines.html')

@app.route('/about')
def about(): return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)