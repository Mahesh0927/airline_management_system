# AirLine Management System

This project is about developing an Airport Management system using Python. The application will help in managing the operations of an airport, such as booking and managing passengers.

## Requirements

* Python 3.x (above)
* MySQL (Workbench)

## Installation

1. To implement the PDF invoice generation install the dependency "pip install fpdf2"
2. Install the library: pip install thefuzz
3. Create the database with the command `python manage.py migrate`
4. Update the database configuration in the file `connect.py`
   
   **Database Configuration Parameters**
* Into the connect.py file add your MySQL database credentials as follow
* DBUSER = "root" #PUT YOUR MySQL username here - usually admin
* DBPASS = "" #PUT YOUR PASSWORD HERE
* DBHOST = "localhost" #PUT YOUR sqlconnection String here
* DBPORT = "3306"
* DBNAME = "airline_db"

## Usage
1. Explore and Copy the content of "sqlQuery.sql" file and paste to the workbench and run all querries
2. Copy content of "dummy.sql" file past and run all querries
3. Open "seeder.py" file and run this file (for inserting the bulk data for flights (arr/dep) for the next 15 days from today )NOTE :- after next 15 days u need to tuncate all the data and re-run this file for next 15 days records
4. open "booking_payment_seeder.py" file run this file (for randome dummy flight booking records with the help of dummy users )
5. Start the server by executing `python manage.py runserver` or run button available at the top right   corner of vs code editor
6. Open the browser and go to `http://127.0.0.1:5000`
7. Login with the credentials created in installation
8. You are now ready to use the application

## Database Configuration

You can set up the database configuration in the file `connect.py`


## Contribute

If you want to contribute to this project, feel free to fork the repository and make pull requests.

# admin

Username :- admin@boundless.com
Passward :- admin123
