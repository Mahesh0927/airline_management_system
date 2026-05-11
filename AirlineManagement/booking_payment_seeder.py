import mysql.connector
import random
import uuid
from datetime import datetime, timedelta

def run_booking_seeder():
    try:
       # Establish connection using your connect.py
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="airline_db"
        )
        cur = db.cursor()


        print("--- Boundless Air: Massive Booking & Payment Seeder ---")

        # 1. Configuration
        TOTAL_TO_GENERATE = random.randint(1000, 1200)
        USER_IDS = list(range(6, 106)) # User IDs 6 to 105
        
        PASSENGER_NAMES = [
            "Aarav Sharma", "Vivaan Verma", "Aditya Singh", "Vihaan Gupta", "Arjun Mehta", "Sai Kumar", "Krishna Iyer", "Ishaan Nair",
            "Rohan Patil", "Rahul Joshi", "Karan Malhotra", "Yash Deshmukh", "Manish Tiwari", "Deepak Yadav", "Amit Kulkarni", "Suresh Reddy",
            "Ankit Jain", "Mohit Agarwal", "Ravi Shukla", "Pankaj Saxena", "Harsh Vardhan", "Nikhil Kapoor", "Varun Bansal", "Abhishek Mishra",
            "Neha Sharma", "Priya Verma", "Ananya Singh", "Sneha Gupta", "Pooja Mehta", "Kavya Iyer", "Divya Nair", "Aisha Khan",
            "Meera Reddy", "Ritu Jain", "Shreya Agarwal", "Nisha Shukla", "Komal Saxena", "Tanya Kapoor", "Simran Kaur", "Preeti Yadav",
            "Rakesh Sharma", "Sunil Verma", "Rajesh Singh", "Mukesh Gupta", "Anil Mehta", "Prakash Iyer", "Sanjay Nair", "Vinod Reddy",
            "Geeta Sharma", "Suman Verma", "Lata Singh", "Rekha Gupta", "Sunita Mehta", "Radha Iyer", "Anita Nair", "Kiran Reddy"
            "Ajay Patil","Vijay Joshi","Dinesh Kulkarni","Mahesh Deshmukh","Ganesh Shinde","Nilesh Pawar","Pravin More","Santosh Jadhav"
            "Rituja Patil","Pallavi Joshi","Snehal Kulkarni","Vaishali Deshmukh","Shruti Shinde","Pooja Pawar","Neha More","Aarti Jadhav"
            "Imran Khan","Salman Sheikh","Asif Ali","Farhan Ansari","Sameer Pathan","Nadeem Shaikh","Zaid Qureshi","Faizan Khan"
            "John Dsouza","Peter Fernandes","Albert Dmello","Joseph Pinto","Michael Lobo","Andrew Rodrigues","Victor Mascarenhas","Francis Noronha"
            "Rohit Kumar","Jitesh Patil","Arun Gavali","Siddharth Joshi","Aman Sharma","Sourabh Sutar","Deepak Patil","Manda Kohali"
            "Akash Panjwani","Manoj Shaha","Rahul Sharma","Mahesh Nikam"
        ]

        # 2. Fetch valid flight data (using positional selection)
        print("Fetching valid flight data...")
        cur.execute("SELECT id, base_price, discount_pct FROM flights ORDER BY RAND() LIMIT 2000")
        valid_flights = cur.fetchall()
        
        if not valid_flights:
            print("Error: No flights found. Please seed flights table first.")
            return

        bookings_batch = []
        
        # 3. Generate Bookings
        print(f"Generating {TOTAL_TO_GENERATE} bookings...")
        for i in range(TOTAL_TO_GENERATE):
            # Select random items
            flight = random.choice(valid_flights)
            u_id = random.choice(USER_IDS)
            
            # Extract by index to avoid 'str' index error
            f_id = flight[0]
            f_base_price = float(flight[1])
            f_discount_pct = int(flight[2])

            p_name = random.choice(PASSENGER_NAMES)
            age = random.randint(2, 85)
            gender = random.choice(['Male', 'Female'])
            
            # Seat & Class logic
            seat_row = random.randint(1, 25)
            seat_num = f"{seat_row}{random.choice(['A','B','C','D','E','F'])}"
            
            if seat_row <= 4:
                b_class, premium = "First", 10000
            elif seat_row <= 10:
                b_class, premium = "Business", 4500
            else:
                b_class, premium = "Economy", 0
                
            # Pricing Calculation
            price_after_disc = (f_base_price * (1 - (f_discount_pct/100))) + premium
            total_paid = price_after_disc + (price_after_disc * 0.18) + 250 # Price + Tax + Fee
            
            # Dates
            b_date = datetime.now() - timedelta(days=random.randint(0, 40))
            dob = b_date - timedelta(days=age*365)
            status = random.choices(['Confirmed', 'Cancelled'], weights=[92, 8])[0]

            bookings_batch.append((
                u_id, f_id, p_name, age, gender, seat_num, b_class, 
                total_paid, b_date, f"ID{random.randint(1000,9999)}", "Indian", 
                dob, f"98700{random.randint(10000,99999)}", status
            ))

        # Perform Batch Insert for Bookings
        cur.executemany("""
            INSERT INTO bookings (user_id, flight_id, passenger_name, passenger_age, passenger_gender, 
            seat_num, class, total_paid, booking_date, gov_id, nationality, dob, phone_num, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, bookings_batch)
        db.commit()

        # 4. Finalizing payment records for the last inserted batch
        print("Creating linked payment records...")
        cur.execute("SELECT id, total_paid, booking_date FROM bookings ORDER BY id DESC LIMIT %s", (TOTAL_TO_GENERATE,))
        new_bookings = cur.fetchall()
        
        payments_batch = []
        methods = ["UPI", "Credit Card", "Debit Card", "Net Banking"]
        
        for nb in new_bookings:
            trans_id = f"BA-{uuid.uuid4().hex[:8].upper()}"
            payments_batch.append((
                nb[0], # id
                trans_id, 
                random.choice(methods), 
                nb[1], # total_paid
                nb[2]  # booking_date
            ))
            
        cur.executemany("""
            INSERT INTO payments (booking_id, transaction_id, payment_method, amount_paid, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, payments_batch)
        
        db.commit()
        print(f"SUCCESS: {TOTAL_TO_GENERATE} Bookings and Payments generated!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_booking_seeder()