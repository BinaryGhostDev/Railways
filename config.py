import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ticket_booking"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None