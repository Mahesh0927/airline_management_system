CREATE DATABASE IF NOT EXISTS airline_db;
USE airline_db;

-- 1. Airports Table
CREATE TABLE airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) UNIQUE,
    name VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100)
);

-- 2. Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role ENUM('user', 'admin') DEFAULT 'user',
    phone VARCHAR(20),
    is_blocked BOOLEAN DEFAULT FALSE
);

-- 3. Bookings Table
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
	flight_id INT,
    passenger_name VARCHAR(100),
    passenger_age INT,
    passenger_gender VARCHAR(10),
    seat_num VARCHAR(10),
    class VARCHAR(20),
	total_paid DECIMAL(10,2),
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    gov_id VARCHAR(50),
    nationality VARCHAR(50),
    dob DATE,
    phone_num VARCHAR(20),
	medical_info TEXT,
	infant_details VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'Confirmed'
);

-- 4. Flights Table
CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airline VARCHAR(50),
    flight_num VARCHAR(10),
    dep_code VARCHAR(10),
    arr_code VARCHAR(10),
    dep_time DATETIME,
    arr_time DATETIME,
    base_price DECIMAL(10,2),
    discount_pct INT DEFAULT 0,
    FOREIGN KEY (dep_code) REFERENCES airports(code),
    FOREIGN KEY (arr_code) REFERENCES airports(code),
    status ENUM('Scheduled', 'Delayed', 'Landed', 'Cancelled') DEFAULT 'Scheduled'
);

-- 5. Airline_info Table
CREATE TABLE airline_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    logo_url VARCHAR(255),
    tagline VARCHAR(100),
    services TEXT, -- Comma separated list like "Free Meals, Wi-Fi"
    facilities TEXT, -- Long description
    baggage_limit VARCHAR(50)
);

-- 6.Payments Table
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    transaction_id VARCHAR(100) UNIQUE,
    payment_method VARCHAR(50),
    amount_paid DECIMAL(10,2),
    payment_status VARCHAR(20) DEFAULT 'Success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- 7.Promo Codes Table
CREATE TABLE promos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE,
    discount_pct INT,
    expiry_date DATE,
    status ENUM('Active', 'Expired') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.Notifications Table
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT,
    type ENUM('Alert', 'Promotion', 'Update'),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Speed up the airport joins
CREATE INDEX idx_flights_dep ON flights(dep_code);
CREATE INDEX idx_flights_arr ON flights(arr_code);

-- Speed up the booking counts
CREATE INDEX idx_bookings_flight ON bookings(flight_id);

-- Add Default Admin
INSERT INTO users (name, email, password, role) VALUES ('System Admin', 'admin@boundless.com', 'admin123', 'admin');

-- FOR REMOVING THE PAST MONTH AIRLINE DETAILS
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE bookings;
truncate table flights;
SET FOREIGN_KEY_CHECKS = 1;
alter table flights auto_increment=1;
