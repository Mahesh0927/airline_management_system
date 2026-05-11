from flask import Blueprint, request, jsonify, session
from db_utils import getCursor
from thefuzz import process
from datetime import datetime
import re

chatbot_bp = Blueprint('chatbot', __name__)

# ==========================================================
# 1. DATA MAPS & KNOWLEDGE BASE
# ==========================================================
AIRPORT_MAP = {
    "mumbai": "BOM", "pune": "PNQ", "nagpur": "NAG", "aurangabad": "IXU",
    "nashik": "ISK", "kolhapur": "KLH", "shirdi": "SAG", "delhi": "DEL",
    "bangalore": "BLR", "mangalore": "IXE", "hubballi": "HBX", "belagavi": "IXG",
    "mysuru": "MYQ", "chennai": "MAA", "coimbatore": "CJB", "madurai": "IXM",
    "tiruchirappalli": "TRZ", "salem": "SXV", "lucknow": "LKO", "varanasi": "VNS",
    "kushinagar": "KBK", "agra": "AGR", "kanpur": "KNU", "ahmedabad": "AMD",
    "surat": "STV", "vadodara": "BDQ", "rajkot": "RAJ", "bhavnagar": "BHU",
    "kolkata": "CCU", "bagdogra": "IXB", "jaipur": "JAI", "jodhpur": "JDH",
    "udaipur": "UDR", "bikaner": "BKB", "kochi": "COK", "trivandrum": "TRV",
    "kozhikode": "CCJ", "kannur": "CNN", "hyderabad": "HYD", "visakhapatnam": "VTZ",
    "vijayawada": "VGA", "tirupati": "TIR", "amritsar": "ATQ", "chandigarh": "IXC",
    "patna": "PAT", "gaya": "GAY", "guwahati": "GAU", "dibrugarh": "DIB"
}

# ==========================================================
# 1. KNOWLEDGE BASE & INTENT MAPPING
# ==========================================================
INTENT_MAP = {
    "greet": ["hi", "hello", "hey", "namaste", "good morning"],
    "auth": ["login", "sign in", "register", "signup", "don't have account", "credentials", "account"],
    "search": ["search", "find", "flights", "available", "fly from", "go to"],
    "booking": ["how to book", "booking process", "steps", "procedure", "guide", "help me book", "process to book"],
    "status": ["track", "status", "delayed", "where is my plane"],
    "cancel": ["cancel", "refund", "reschedule", "money back"],
    "baggage": ["luggage", "weight", "bag", "limit", "allowance"],
    "payment": ["payment methods", "how to pay", "upi", "credit card", "debit card", "net banking", "wallets"],
    "offers": ["offers", "promo", "discount", "code", "coupon"],
    "bookings": ["my bookings", "history", "tickets", "my trips"]
}

KB = {
    "booking": "✈️ **Booking Process:**\n1. **Login/Register** to your account.\n2. **Search** for flights on the Home page.\n3. **Select** your flight and enter details.\n4. **Select** your seat and **Pay** securely.\n5. **Download** your E-ticket!",
    "payment": "💳 **Supported Payment Methods:**\n• **UPI**: Google Pay, PhonePe, Paytm\n• **Cards**: All Debit & Credit Cards (Visa, MasterCard, RuPay)\n• **Net Banking**: All major Indian Banks\n• **Wallets**: Amazon Pay, Mobikwik",
    "register": "No account? No problem! 😊\nYou can create a new account here to start booking flights:\n[Register]",
    "baggage": "🧳 **Baggage Policy:**\n• Economy: 15kg Check-in / 7kg Cabin\n• Business: 25kg Check-in / 10kg Cabin"
}

# ==========================================================
# 2. CORE LOGIC ENGINE (BUG-FIXED)
# ==========================================================

def identify_intent(msg):
    msg = msg.lower().strip()
    
    # --- PHASE 1: DIRECT PHRASE MATCHING (Highest Accuracy) ---
    if any(x in msg for x in ["how to book", "how i can book", "booking process"]): return "booking"
    if any(x in msg for x in ["payment", "how to pay", "pay via"]): return "payment"
    if any(x in msg for x in ["don't have", "no account", "credentials", "create account"]): return "auth"
    if any(x in msg for x in ["my bookings", "my history", "my tickets"]): return "bookings"
    if any(x in msg for x in ["status", "track", "delayed"]): return "status"

    # --- PHASE 2: FUZZY MATCHING (Typo Tolerance) ---
    all_keywords = [k for sublist in INTENT_MAP.values() for k in sublist]
    match, score = process.extractOne(msg, all_keywords)
    
    if score > 70:
        for intent, keywords in INTENT_MAP.items():
            if match in keywords: return intent
            
    return "unknown"

def extract_route(msg):
    clean_msg = msg.lower().replace("from", " ").replace("to", " ")
    found = [city for city in AIRPORT_MAP.keys() if city in clean_msg]
    return (found[0], found[1]) if len(found) >= 2 else (None, None)

# ==========================================================
# 3. CHATBOT QUERY ROUTE
# ==========================================================

@chatbot_bp.route('/chatbot/query', methods=['POST'])
def chatbot_query():
    user_msg = request.json.get("message", "").lower().strip()
    user_id = session.get("user_id")
    user_name = session.get("user_name", "Guest")
    
    intent = identify_intent(user_msg)
    res = {"text": "", "quick_replies": []}

    # 1. GREETING
    if intent == "greet" or user_msg == "hello_trigger":
        res["text"] = f"Namaste {user_name}! 👋 Welcome to **BoundlessAir**. How can I assist you today?"
        res["quick_replies"] = ["Search Flights", "How to Book?", "Latest Offers"]

    # 2. AUTH / REGISTER
    elif intent == "auth":
        if user_id:
            res["text"] = "You are already logged in to your account! You can manage your trips from the dashboard."
            res["quick_replies"] = ["My Bookings", "Search Flights"]
        else:
            res["text"] = "I understand. If you don't have an account, please **Register** first. If you have one, please **Login** to continue booking."
            res["quick_replies"] = ["Login Now", "Register"]

    # 3. BOOKING GUIDE
    elif intent == "booking":
        res["text"] = KB["booking"]
        if not user_id:
            res["text"] += "\n\n⚠️ **Note:** Please Login to start a new booking."
            res["quick_replies"] = ["Login Now", "Search Flights"]
        else:
            res["quick_replies"] = ["Search Flights", "My Bookings"]

    # 4. PAYMENT METHODS
    elif intent == "payment":
        res["text"] = KB["payment"]
        res["quick_replies"] = ["How to Book?", "Offers"]

    # 5. MY BOOKINGS / HISTORY (SENSITIVE DATA)
    elif intent in ["bookings", "status"]:
        if not user_id:
            res["text"] = f"To access your **{intent}** details and flight history, please **Login to know more** 🔐"
            res["quick_replies"] = ["Login Now", "Register"]
        else:
            cur = getCursor()
            cur.execute("""
                SELECT f.flight_num, b.status, a1.city as src, a2.city as dst 
                FROM bookings b JOIN flights f ON b.flight_id=f.id 
                JOIN airports a1 ON f.dep_code=a1.code JOIN airports a2 ON f.arr_code=a2.code 
                WHERE b.user_id=%s ORDER BY b.booking_date DESC LIMIT 1
            """, (user_id,))
            b = cur.fetchone()
            if b:
                res["text"] = f"Your latest flight **{b['flight_num']}** ({b['src']} → {b['dst']}) is **{b['status']}**."
            else:
                res["text"] = "You don't have any bookings in your history yet."
            res["quick_replies"] = ["Search Flights", "Go to Dashboard"]

    # 6. SEARCH FLIGHT
    elif intent == "search":
        src, dst = extract_route(user_msg)
        if src and dst:
            cur = getCursor()
            cur.execute("SELECT airline, flight_num, base_price FROM flights WHERE dep_code=%s AND arr_code=%s AND dep_time > NOW() LIMIT 2", (AIRPORT_MAP[src], AIRPORT_MAP[dst]))
            flights = cur.fetchall()
            if flights:
                res["text"] = f"✈️ **Flights from {src.title()} to {dst.title()}:**\n" + "\n".join([f"• {f['airline']} ({f['flight_num']}) @ ₹{f['base_price']}" for f in flights])
                res["quick_replies"] = ["Book Now", "Main Menu"]
            else:
                res["text"] = f"Sorry, no direct flights found for {src.title()} to {dst.title()} right now."
        else:
            res["text"] = "I can find flights for you! 🛫 Tell me: **'Flights from Mumbai to Delhi'**.\n\n⚠️ **Note:** Booking requires login."
            res["quick_replies"] = ["Login Now", "Register"]

    # 7. OFFERS
    elif intent == "offers":
        res["text"] = "🎁 **Current Offers:**\n• **FLY15**: 15% OFF\n• **WELCOME10**: 10% OFF\n\nReady to book?"
        res["quick_replies"] = ["Book Now", "Main Menu"]

    # 8. FALLBACK
    else:
        res["text"] = "I'm still learning! ☁️ You can ask about:\n• 'How to book'\n• 'Payment methods'\n• 'Baggage rules'"
        res["quick_replies"] = ["How to Book?", "Baggage Rules", "Support"]

    return jsonify(res)