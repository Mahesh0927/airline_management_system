import mysql.connector
from datetime import datetime, timedelta
import random

def run_complete_mesh_seeder():
    try:
        # Establish connection using your connect.py
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="airline_db"
        )
        cur = db.cursor()

        print("--- Boundless Air: Complete Route Seeder (15 Days) ---")
        
        # 1. Fetch all airports
        cur.execute("SELECT code FROM airports")
        airports = [row[0] for row in cur.fetchall()]
        
        if not airports:
            print("Error: No airports found. Please ensure your airport table is populated.")
            return

        # 2. Configuration
        airlines = ["IndiGo", "Air India", "Vistara", "SpiceJet", "Akasa Air", "Air India Express"]
        batch_data = []
        days_to_seed = 15
        flights_per_route = 10
        
        print(f"Total Airports: {len(airports)}")
        print(f"Total Routes to generate: {len(airports) * (len(airports) - 1)}")
        
        # 3. Clear old data
        print("Clearing existing flight records for a clean start...")
        cur.execute("DELETE FROM flights")

        # 4. Triple Loop: Day -> Departure -> Arrival
        for day_offset in range(0, days_to_seed):
            date_obj = datetime.now() + timedelta(days=day_offset)
            date_str = date_obj.strftime('%Y-%m-%d')
            
            print(f"Generating for {date_str}...")

            for dep in airports:
                for arr in airports:
                    if dep == arr:
                        continue # Skip same-city flights
                    
                    # Create 15 flights for this specific pair
                    for i in range(flights_per_route):
                        airline = random.choice(airlines)
                        f_num = f"{airline[:2].upper()}-{random.randint(1000, 9999)}"
                        
                        # Spread flights across the day
                        hour = random.randint(0, 23)
                        minute = random.choice([0, 15, 30, 45])
                        
                        dep_dt = datetime.strptime(f"{date_str} {hour:02}:{minute:02}:00", '%Y-%m-%d %H:%M:%S')
                        
                        # Random duration (1 to 4 hours)
                        duration = random.randint(60, 240)
                        arr_dt = dep_dt + timedelta(minutes=duration)
                        
                        price = random.randint(3000, 14000)
                        discount = random.choice([0, 0, 5, 10, 15, 20])

                        batch_data.append((
                            airline, f_num, dep, arr, 
                            dep_dt.strftime('%Y-%m-%d %H:%M:%S'), 
                            arr_dt.strftime('%Y-%m-%d %H:%M:%S'), 
                            price, discount
                        ))

                        # Batch Insert every 10,000 records for high performance
                        if len(batch_data) >= 10000:
                            query = """INSERT INTO flights 
                                       (airline, flight_num, dep_code, arr_code, dep_time, arr_time, base_price, discount_pct) 
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                            cur.executemany(query, batch_data)
                            db.commit()
                            batch_data = []

        # Insert remaining records
        if batch_data:
            cur.executemany(query, batch_data)
            db.commit()

        print("\nSUCCESS: The database is now fully populated!")
        print("Every airport in India now has 15 daily flights to every other airport.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if db.is_connected():
            cur.close()
            db.close()

if __name__ == "__main__":
    run_complete_mesh_seeder()