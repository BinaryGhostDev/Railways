import mysql.connector
from config import connect_to_database  # Assuming you have a connect_to_database function in your config module

def create_train_booking_tables(connection):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                first_name VARCHAR(255),
                middle_name VARCHAR(255),
                last_name VARCHAR(255),
                occupation VARCHAR(255),
                country VARCHAR(255),
                gender VARCHAR(10),
                email VARCHAR(255) UNIQUE,
                mobile_number VARCHAR(20) UNIQUE,
                address TEXT,
                wallet DECIMAL(10, 2) DEFAULT 0.0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                boarding_station_name VARCHAR(255) NOT NULL,
                boarding_station_code VARCHAR(10) NOT NULL,
                destination_station_name VARCHAR(255) NOT NULL,
                destination_station_code VARCHAR(10) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trains (
                id INT AUTO_INCREMENT PRIMARY KEY,
                boarding_station_code VARCHAR(10) NOT NULL,
                destination_station_code VARCHAR(10) NOT NULL,
                train_name VARCHAR(255) NOT NULL,
                Departure TIME NOT NULL,
                Arrival TIME NOT NULL,
                `SL Fare` INT NOT NULL,
                `1A Fare` INT NOT NULL,
                `2A Fare` INT NOT NULL,
                `3A Fare` INT NOT NULL,
                `SL Seats` INT DEFAULT 0,
                `1A Seats` INT DEFAULT 0,
                `2A Seats` INT DEFAULT 0,
                `3A Seats` INT DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INT AUTO_INCREMENT PRIMARY KEY,
                booked_username VARCHAR(255) NOT NULL,
                booked_user_id INT NOT NULL,
                train_id INT NOT NULL,
                PNR INT NOT NULL,
                passenger_name VARCHAR(255) DEFAULT NULL,
                dob DATE DEFAULT NULL,
                aadhar_number INT NOT NULL,
                mobile_number INT NOT NULL,
                boarding_station_code VARCHAR(10) DEFAULT NULL,
                destination_station_code VARCHAR(10) DEFAULT NULL,
                train_name VARCHAR(255) DEFAULT NULL,
                Departure TIME NOT NULL,
                Arrival TIME NOT NULL,
                seat_class VARCHAR(20) NOT NULL,
                seat VARCHAR(3) DEFAULT NULL,
                fare INT DEFAULT NULL,
                payment_status VARCHAR(20) DEFAULT NULL,
                journey_date DATE NOT NULL,
                status VARCHAR(20) NOT NULL,
                booked_time DATETIME DEFAULT NULL,
                FOREIGN KEY (train_id) REFERENCES trains(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT(11) NOT NULL,
                transaction_id VARCHAR(12),
                amount DECIMAL(10,2),
                status VARCHAR(20) DEFAULT 'PENDING',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password_hash VARCHAR(255),
                full_name VARCHAR(255) NOT NULL
            )
        """)

        connection.commit()
        cursor.close()
        # print("Tables created or updated successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def main():
    connection = connect_to_database()

    if connection:
        create_train_booking_tables(connection)

if __name__ == "__main__":
    main()
