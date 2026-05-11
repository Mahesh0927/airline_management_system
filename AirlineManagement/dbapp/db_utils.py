from flask import g
import mysql.connector
import connect

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=connect.dbhost,
            user=connect.dbuser,
            password=connect.dbpass,
            database=connect.dbname,
            autocommit=True
        )
    return g.db

def getCursor():
    db = get_db()
    return db.cursor(dictionary=True)