import mysql.connector
from config import connect_to_database
from hashlib import sha256
from prettytable import PrettyTable
from src.text_color import success_message, error_message
from src.admin_manage_tickets import Manage_Booked_Tickets
from src.admin_manage_users import manage_users_menu
from src.manage_admin import manage_admins_menu


def Add_Trains_With_Routes(cursor, connection):
    print("\nAdd Trains with Routes:")

    # Collecting input data
    boarding_station_name = input("Enter Boarding Station Name: ")
    boarding_station_code = input("Enter Boarding Station Code: ")
    destination_station_name = input("Enter Destination Station Name: ")
    destination_station_code = input("Enter Destination Station Code: ")
    train_name = input("Enter Train Name: ")
    departure_time = input("Enter Departure Time (HH:MM): ")
    arrival_time = input("Enter Arrival Time (HH:MM): ")
    sl_fare = int(input("Enter SL Fare: "))
    a1_fare = int(input("Enter 1A Fare: "))
    a2_fare = int(input("Enter 2A Fare: "))
    a3_fare = int(input("Enter 3A Fare: "))
    sl_seats = int(input("Enter SL Seats: "))
    a1_seats = int(input("Enter 1A Seats: "))
    a2_seats = int(input("Enter 2A Seats: "))
    a3_seats = int(input("Enter 3A Seats: "))

    try:
        # Insert data into stations table
        cursor.execute("""
            INSERT INTO stations (boarding_station_name, boarding_station_code, destination_station_name, destination_station_code)
            VALUES (%s, %s, %s, %s)
        """, (boarding_station_name, boarding_station_code, destination_station_name, destination_station_code))

        # Insert data into trains table
        cursor.execute("""
            INSERT INTO trains (boarding_station_code, destination_station_code, train_name, Departure, Arrival, 
                                `SL Fare`, `1A Fare`, `2A Fare`, `3A Fare`, `SL Seats`, `1A Seats`, `2A Seats`, `3A Seats`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (boarding_station_code, destination_station_code, train_name, departure_time, arrival_time,
              sl_fare, a1_fare, a2_fare, a3_fare, sl_seats, a1_seats, a2_seats, a3_seats))

        connection.commit()

        success_message("Train with Routes added successfully!")
    except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
     error_message("\n\nExiting due to user interruption. Goodbye!")

    except mysql.connector.Error as err:
        error_message(f"Error: {err}")



def Verify_Payments(cursor, connection):
    try:
        # Fetch all transactions with PENDING status
        cursor.execute("""
            SELECT * FROM transactions
            WHERE status = 'PENDING'
        """)
        transactions = cursor.fetchall()

        if not transactions:
            print("No pending payments to verify.")
            return

        # Display transactions in a pretty table
        table = PrettyTable()
        table.field_names = ["ID", "User ID", "Transaction ID", "Amount", "Status", "Created At"]

        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[2],
                           transaction[3], transaction[4], transaction[5]])

        print(table)

        # Ask admin to choose a payment to verify
        transaction_id_to_verify = input("Enter the ID of the transaction to verify: ")

        # Check if the selected transaction is already verified
        cursor.execute("""
            SELECT status FROM transactions
            WHERE id = %s
        """, (transaction_id_to_verify,))
        status = cursor.fetchone()

        if not status or status[0] == 'VERIFIED':
            print("Invalid transaction ID or transaction already verified.")
            return

        # Update status to VERIFIED in transactions table
        cursor.execute("""
            UPDATE transactions
            SET status = 'VERIFIED'
            WHERE id = %s
        """, (transaction_id_to_verify,))

        # Fetch user ID and amount from the verified transaction
        cursor.execute("""
            SELECT user_id, amount FROM transactions
            WHERE id = %s
        """, (transaction_id_to_verify,))
        transaction_data = cursor.fetchone()

        if transaction_data:
            user_id = transaction_data[0]
            amount = transaction_data[1]

            # Update wallet in users table by adding the verified amount
            cursor.execute("""
                UPDATE users
                SET wallet = wallet + %s
                WHERE id = %s
            """, (amount, user_id))

            connection.commit()
            print(f"Payment with ID {transaction_id_to_verify} verified successfully.")

    except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
     error_message("\n\nExiting due to user interruption. Goodbye!")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def main():
    connection = connect_to_database()

    if connection:
        try:
            cursor = connection.cursor()
            Verify_Payments(cursor, connection)

        finally:
            cursor.close()
            connection.close()



def login_admin(cursor, connection):
    while True:
        print("\nAdmin Login:")
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Hash the entered password for comparison
        password_hash = sha256(password.encode()).hexdigest()

        try:
            cursor.execute("""
                SELECT * FROM admin
                WHERE username = %s AND password_hash = %s
            """, (username, password_hash))

            admin = cursor.fetchone()

            if admin:
                admin_id, admin_username, _, full_name, status = admin

                if status == 'ACTIVE':
                    print("\nLogin Successful!")
                    print(f"User ID: {admin_id}")
                    print(f"Username: {admin_username}")
                    print(f"Full Name: {full_name}")
                    print(f"Status: {status}")

                    admin_menu(cursor, connection)  # Pass cursor and connection to admin_menu
                    break  # Break the loop after a successful login
                elif status == 'BLOCKED':
                    print("")
                    error_message(f'''Dear Admin, {full_name}
Your account has been blocked by our Railways Department. We apologize for the inconvenience.
You do not have permission to login.''')
                else:
                    error_message("Access denied. Unknown admin status.")
            else:
                error_message("Invalid username or password. Please try again.")

        except KeyboardInterrupt:
            # Handle KeyboardInterrupt (Ctrl+C)
            error_message("\n\nExiting due to user interruption. Goodbye!")

        except mysql.connector.Error as err:
            error_message(f"Error: {err}")
            break  # Break the loop in case of an error

def add_new_admin(cursor, connection):
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")
    full_name = input("Enter Admin Full Name: ")

    # Hash the password using SHA-256
    password_hash = sha256(password.encode()).hexdigest()

    try:
        cursor.execute("""
            INSERT INTO admin (username, password_hash, full_name)
            VALUES (%s, %s, %s)
        """, (username, password_hash, full_name))

        connection.commit()

        success_message("Admin registered successfully!")

    except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
     error_message("\n\nExiting due to user interruption. Goodbye!")

    except mysql.connector.Error as err:
        error_message(f"Error: {err}")

def admin_menu(cursor, connection):

    try:
        while True:
            print("")
            print("1. Add New Admin")
            print("2. Add Trains With Routes")
            print("3. Verify Payments")
            print("4. Manage Booked Tickets")
            print("5. Manage Users")
            print("6. Manage Admins")
            print("7. Log Out")
            print("")
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                add_new_admin(cursor, connection)
            # Add other menu options and their corresponding function calls
            elif choice == '2':
                Add_Trains_With_Routes(cursor, connection)
            elif choice == '3':
                Verify_Payments(cursor, connection)
            elif choice == '4':
                Manage_Booked_Tickets(connection, cursor)
            elif choice == '5':
                manage_users_menu(connection, cursor)
            elif choice == '6':
                manage_admins_menu(connection, cursor)
            elif choice == '7':
                success_message("Logging out. Goodbye!")
                break
            else:
                error_message("Invalid choice. Please enter a valid option.")

    except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
     error_message("\n\nExiting due to user interruption. Goodbye!")

def main():
    connection = connect_to_database()

    if connection:
        try:
            cursor = connection.cursor()
            login_admin(cursor, connection)

        finally:
            cursor.close()
            connection.close()

main()
