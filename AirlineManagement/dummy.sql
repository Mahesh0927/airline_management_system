-- Airline Info Table
INSERT INTO airline_info (name, tagline, services, facilities, baggage_limit) VALUES 
('IndiGo', 'Go IndiGo!', 'Web Check-in, 6E Eats, Punctual Service', 'Standard Legroom, In-flight snacks for purchase, USB Charging', '15kg Check-in'),
('Air India', 'Truly Indian', 'Hot Meals, Extra Baggage, Luxury Cabins', 'Spacious Seats, Complimentary Alcoholic Beverages, In-flight Movies', '25kg Check-in'),
('Vistara', 'Fly the New Feeling', 'Premium Economy, Starbucks Coffee, Live TV', 'Mood Lighting, Personal Entertainment Screen, Gourmet Meals', '20kg Check-in'),
('SpiceJet', 'Red. Hot. Spicy.', 'SpiceMax Seats, Pre-booked Meals', 'Extra Legroom (SpiceMax), Quick Boarding, On-board Cafe', '15kg Check-in'),
('Akasa Air', 'Its Your Sky', 'Eco-friendly, Fresh Meals', 'Newer Aircraft, Quiet Cabin, USB Charging at every seat', '15kg Check-in');

-- AIRPORT DATA INSERTION (State-wise)
INSERT INTO airports VALUES 
('BOM','Chhatrapati Shivaji Maharaj Intl','Mumbai','Maharashtra'),
('PNQ','Pune Airport','Pune','Maharashtra'),
('NAG','Dr. Babasaheb Ambedkar Intl','Nagpur','Maharashtra'),
('IXU','Aurangabad Airport','Aurangabad','Maharashtra'),
('ISK','Nashik Airport','Nashik','Maharashtra'),
('KLH','Kolhapur Airport','Kolhapur','Maharashtra'),
('SAG','Shirdi Airport','Shirdi','Maharashtra'),
('DEL','Indira Gandhi International','Delhi','Delhi'),
('BLR','Kempegowda International','Bangalore','Karnataka'),
('IXE','Mangaluru International','Mangalore','Karnataka'),
('HBX','Hubballi Airport','Hubballi','Karnataka'),
('IXG','Belagavi Airport','Belagavi','Karnataka'),
('MYQ','Mysuru Airport','Mysuru','Karnataka'),
('MAA','Chennai International','Chennai','Tamil Nadu'),
('CJB','Coimbatore International','Coimbatore','Tamil Nadu'),
('IXM','Madurai Airport','Madurai','Tamil Nadu'),
('TRZ','Tiruchirappalli International','Tiruchirappalli','Tamil Nadu'),
('SXV','Salem Airport','Salem','Tamil Nadu'),
('LKO','Chaudhary Charan Singh Intl','Lucknow','Uttar Pradesh'),
('VNS','Lal Bahadur Shastri Intl','Varanasi','Uttar Pradesh'),
('KBK','Kushinagar International','Kushinagar','Uttar Pradesh'),
('AGR','Agra Airport','Agra','Uttar Pradesh'),
('KNU','Kanpur Airport','Kanpur','Uttar Pradesh'),
('AMD','Sardar Vallabhbhai Patel Intl','Ahmedabad','Gujarat'),
('STV','Surat Airport','Surat','Gujarat'),
('BDQ','Vadodara Airport','Vadodara','Gujarat'),
('RAJ','Rajkot Airport','Rajkot','Gujarat'),
('BHU','Bhavnagar Airport','Bhavnagar','Gujarat'),
('CCU','Netaji Subhas Chandra Bose Intl','Kolkata','West Bengal'),
('IXB','Bagdogra Airport','Bagdogra','West Bengal'),
('JAI','Jaipur International','Jaipur','Rajasthan'),
('JDH','Jodhpur Airport','Jodhpur','Rajasthan'),
('UDR','Udaipur Airport','Udaipur','Rajasthan'),
('BKB','Bikaner Airport','Bikaner','Rajasthan'),
('COK','Cochin International','Kochi','Kerala'),
('TRV','Trivandrum International','Trivandrum','Kerala'),
('CCJ','Calicut International','Kozhikode','Kerala'),
('CNN','Kannur International','Kannur','Kerala'),
('HYD','Rajiv Gandhi International','Hyderabad','Telangana'),
('VTZ','Visakhapatnam Airport','Visakhapatnam','Andhra Pradesh'),
('VGA','Vijayawada Airport','Vijayawada','Andhra Pradesh'),
('TIR','Tirupati Airport','Tirupati','Andhra Pradesh'),
('ATQ','Sri Guru Ram Dass Jee Intl','Amritsar','Punjab'),
('IXC','Chandigarh Airport','Chandigarh','Punjab'),
('PAT','Jay Prakash Narayan Airport','Patna','Bihar'),
('GAY','Gaya Airport','Gaya','Bihar'),
('GAU','Lokpriya Gopinath Bordoloi Intl','Guwahati','Assam'),
('DIB','Dibrugarh Airport','Dibrugarh','Assam')
('BBI', 'Biju Patnaik International Airport', 'Bhubaneswar', 'Odisha'),
('IXR', 'Birsa Munda Airport', 'Ranchi', 'Jharkhand'),
('RPR', 'Raipur Airport', 'Raipur', 'Chhattisgarh'),
('IXZ', 'Veer Savarkar International Airport', 'Port Blair', 'Andaman and Nicobar Islands');

-- Dummy Promos data
INSERT INTO promos (code, discount_pct, expiry_date, status) VALUES 
('FLYBA15', 15, '2026-12-31', 'Active'),       -- Standard sitewide offer
('WELCOME20', 20, '2026-06-30', 'Active'),     -- New user special
('SUMMER25', 25, '2026-05-30', 'Active'),      -- Seasonal Holiday offer
('GOAFREE', 10, '2026-08-15', 'Active'),       -- Destination specific
('EXCLUSIV30', 30, '2026-07-01', 'Active'),    -- Premium member code
('FESTIVE50', 50, '2024-01-01', 'Expired'),    -- Old offer to test 'Expired' UI
('MONSOON10', 10, '2025-09-20', 'Expired'),    -- Testing date logic
('BUSINESS5', 5, '2027-01-01', 'Active');      -- Corporate tie-up

-- Dummy Users data
INSERT INTO users (name, email, password, role, is_blocked) VALUES
('Aarav Sharma','aarav1@gmail.com','password123','user',0),
('Vivaan Verma','vivaan2@gmail.com','password123','user',0),
('Aditya Singh','aditya3@gmail.com','password123','user',0),
('Vihaan Gupta','vihaan4@gmail.com','password123','user',0),
('Arjun Mehta','arjun5@gmail.com','password123','user',0),
('Sai Kumar','sai6@gmail.com','password123','user',0),
('Krishna Iyer','krishna7@gmail.com','password123','user',0),
('Ishaan Nair','ishaan8@gmail.com','password123','user',0),

('Rohan Patil','rohan9@gmail.com','password123','user',0),
('Rahul Joshi','rahul10@gmail.com','password123','user',0),
('Karan Malhotra','karan11@gmail.com','password123','user',0),
('Yash Deshmukh','yash12@gmail.com','password123','user',0),
('Manish Tiwari','manish13@gmail.com','password123','user',0),
('Deepak Yadav','deepak14@gmail.com','password123','user',0),
('Amit Kulkarni','amit15@gmail.com','password123','user',0),
('Suresh Reddy','suresh16@gmail.com','password123','user',0),

('Ankit Jain','ankit17@gmail.com','password123','user',0),
('Mohit Agarwal','mohit18@gmail.com','password123','user',0),
('Ravi Shukla','ravi19@gmail.com','password123','user',0),
('Pankaj Saxena','pankaj20@gmail.com','password123','user',0),
('Harsh Vardhan','harsh21@gmail.com','password123','user',0),
('Nikhil Kapoor','nikhil22@gmail.com','password123','user',0),
('Varun Bansal','varun23@gmail.com','password123','user',0),
('Abhishek Mishra','abhishek24@gmail.com','password123','user',0),

('Neha Sharma','neha25@gmail.com','password123','user',0),
('Priya Verma','priya26@gmail.com','password123','user',0),
('Ananya Singh','ananya27@gmail.com','password123','user',0),
('Sneha Gupta','sneha28@gmail.com','password123','user',0),
('Pooja Mehta','pooja29@gmail.com','password123','user',0),
('Kavya Iyer','kavya30@gmail.com','password123','user',0),
('Divya Nair','divya31@gmail.com','password123','user',0),
('Aisha Khan','aisha32@gmail.com','password123','user',0),

('Meera Reddy','meera33@gmail.com','password123','user',0),
('Ritu Jain','ritu34@gmail.com','password123','user',0),
('Shreya Agarwal','shreya35@gmail.com','password123','user',0),
('Nisha Shukla','nisha36@gmail.com','password123','user',0),
('Komal Saxena','komal37@gmail.com','password123','user',0),
('Tanya Kapoor','tanya38@gmail.com','password123','user',0),
('Simran Kaur','simran39@gmail.com','password123','user',0),
('Preeti Yadav','preeti40@gmail.com','password123','user',0),

('Rakesh Sharma','rakesh41@gmail.com','password123','user',0),
('Sunil Verma','sunil42@gmail.com','password123','user',0),
('Rajesh Singh','rajesh43@gmail.com','password123','user',0),
('Mukesh Gupta','mukesh44@gmail.com','password123','user',0),
('Anil Mehta','anil45@gmail.com','password123','user',0),
('Prakash Iyer','prakash46@gmail.com','password123','user',0),
('Sanjay Nair','sanjay47@gmail.com','password123','user',0),
('Vinod Reddy','vinod48@gmail.com','password123','user',0),

('Geeta Sharma','geeta49@gmail.com','password123','user',0),
('Suman Verma','suman50@gmail.com','password123','user',0),
('Lata Singh','lata51@gmail.com','password123','user',0),
('Rekha Gupta','rekha52@gmail.com','password123','user',0),
('Sunita Mehta','sunita53@gmail.com','password123','user',0),
('Radha Iyer','radha54@gmail.com','password123','user',0),
('Anita Nair','anita55@gmail.com','password123','user',0),
('Kiran Reddy','kiran56@gmail.com','password123','user',0),

('Ajay Patil','ajay57@gmail.com','password123','user',0),
('Vijay Joshi','vijay58@gmail.com','password123','user',0),
('Dinesh Kulkarni','dinesh59@gmail.com','password123','user',0),
('Mahesh Deshmukh','mahesh60@gmail.com','password123','user',0),
('Ganesh Shinde','ganesh61@gmail.com','password123','user',0),
('Nilesh Pawar','nilesh62@gmail.com','password123','user',0),
('Pravin More','pravin63@gmail.com','password123','user',0),
('Santosh Jadhav','santosh64@gmail.com','password123','user',0),

('Rituja Patil','rituja65@gmail.com','password123','user',0),
('Pallavi Joshi','pallavi66@gmail.com','password123','user',0),
('Snehal Kulkarni','snehal67@gmail.com','password123','user',0),
('Vaishali Deshmukh','vaishali68@gmail.com','password123','user',0),
('Shruti Shinde','shruti69@gmail.com','password123','user',0),
('Pooja Pawar','pooja70@gmail.com','password123','user',0),
('Neha More','neha71@gmail.com','password123','user',0),
('Aarti Jadhav','aarti72@gmail.com','password123','user',0),

('Imran Khan','imran73@gmail.com','password123','user',0),
('Salman Sheikh','salman74@gmail.com','password123','user',0),
('Asif Ali','asif75@gmail.com','password123','user',0),
('Farhan Ansari','farhan76@gmail.com','password123','user',0),
('Sameer Pathan','sameer77@gmail.com','password123','user',0),
('Nadeem Shaikh','nadeem78@gmail.com','password123','user',0),
('Zaid Qureshi','zaid79@gmail.com','password123','user',0),
('Faizan Khan','faizan80@gmail.com','password123','user',0),

('John Dsouza','john81@gmail.com','password123','user',0),
('Peter Fernandes','peter82@gmail.com','password123','user',0),
('Albert Dmello','albert83@gmail.com','password123','user',0),
('Joseph Pinto','joseph84@gmail.com','password123','user',0),
('Michael Lobo','michael85@gmail.com','password123','user',0),
('Andrew Rodrigues','andrew86@gmail.com','password123','user',0),
('Victor Mascarenhas','victor87@gmail.com','password123','user',0),
('Francis Noronha','francis88@gmail.com','password123','user',0),

('Rohit Kumar','rohit89@gmail.com','password123','user',0),
('Jitesh Patil','jitesh90@gmail.com','password123','user',0),
('Arun Gavali','arun91@gmail.com','password123','user',0),
('Siddharth Joshi','sidd92@gmail.com','password123','user',0),
('Aman Sharma','aman93@gmail.com','password123','user',0),
('Sourabh Sutar','sourabh94@gmail.com','password123','user',0),
('Deepak Patil','deepak95@gmail.com','password123','user',0),
('Manda Kohali','madan96@gmail.com','password123','user',0),
('Akash Panjwani','akash97@gmail.com','password123','user',0),
('Manoj Shaha','manoj98@gmail.com','password123','user',0),
('Mohammad Shami','mohammad99@gmail.com','password123','admin',0),
('Blocked User','blocked100@gmail.com','password123','user',1);

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