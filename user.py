import bcrypt
import mysql.connector
from src.preloader import letter_animation, progress_bar
from src.Book_Railways_Ticket import book_railways_ticket
from config import connect_to_database
from db import create_train_booking_tables
from src.Booked_Tickets import search_booked_ticket_by_pnr, show_all_booked_tickets, show_all_tickets, cancel_booked_ticket
from src.Add_Balance import add_balance
from src.Update_Details import update_user_details
from src.Profile import view_user_profile
from src.text_color import success_message, error_message

def create_banner(text, color='\033[1;33m'):
    banner_text = f'{color}{text}\033[0m'
    print(banner_text)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(input_password, hashed_password):
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password_bytes)

def register_user(connection):
    print("\nRegisteration Valid for only Indians:")
    print("")
    username = input("Enter username: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    first_name = input("Enter first name: ")
    middle_name = input("Enter middle name (optional): ")
    last_name = input("Enter last name: ")
    occupation = input("Enter occupation: ")
    country = input("Enter country: ")
    gender = input("Enter gender: ")
    email = input("Enter email: ")
    mobile_number = input("Enter mobile number with country code +91 : ")
    address = input("Enter full address: ")

    if password != confirm_password:
        error_message("Error: Passwords do not match.")
        return

    hashed_password = hash_password(password)

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (
                username, password, first_name, middle_name, last_name, 
                occupation, country, gender, email, mobile_number, address
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, hashed_password, first_name, middle_name, last_name,
              occupation, country, gender, email, mobile_number, address))
        connection.commit()
        cursor.close()
        print("")
        success_message("User registered successfully!")
    
    except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
     error_message("\n\nExiting due to user interruption. Goodbye!")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def login_user(connection):
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, username, first_name, middle_name, last_name, password, wallet, occupation, country, gender, email, mobile_number, address, status FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password(password, user['password']) and user['status'] == 'ACTIVE':
            success_message("Login successful!")
            create_banner(r"""
 ____       _ _                           _____ _      _        _     ____              _    _             
|  _ \ __ _(_) |_      ____ _ _   _ ___  |_   _(_) ___| | _____| |_  | __ )  ___   ___ | | _(_)_ __   __ _ 
| |_) / _` | | \ \ /\ / / _` | | | / __|   | | | |/ __| |/ / _ \ __| |  _ \ / _ \ / _ \| |/ / | '_ \ / _` |
|  _ < (_| | | |\ V  V / (_| | |_| \__ \   | | | | (__|   <  __/ |_  | |_) | (_) | (_) |   <| | | | | (_| |
|_| \_\__,_|_|_| \_/\_/ \__,_|\__, |___/   |_| |_|\___|_|\_\___|\__| |____/ \___/ \___/|_|\_\_|_| |_|\__, |
                              |___/                                                                  |___/ 
             """)
            success_message("\nUser details:")
            print(f"User ID: {user['id']}")
            full_name = ' '.join(filter(None, [user['first_name'], user['middle_name'], user['last_name']]))
            print(f"Full Name: {full_name}")
            print(f"Wallet Balance: ₹{user['wallet']:.2f}")
            print(f"Status: {user['status']}")

            while True:
                print("\n1. Book Railways Ticket")
                print("2. Booked Tickets")
                print("3. Add Balance")
                print("4. Profile")
                print("5. Update Details")
                print("6. Logout")

                option = input("Enter your option (1-6): ")

                if option == '1':
                    book_railways_ticket(connection, user)
                elif option == '2':
                    while True:
                        print("\n1. Search Booked Tickets By PNR")
                        print("2. Show All BOOKED Tickets")
                        print("3. Cancel BOOKED Tickets")
                        print("4. Show All Tickets")
                        print("5. Back To Menu")
                        
                        booked_choice = input("Enter your option (1-5): ")
                        if booked_choice == '1':
                            search_booked_ticket_by_pnr(connection, user)
                        elif booked_choice == '2':
                            show_all_booked_tickets(connection, user)
                        elif booked_choice == '3':
                            cancel_booked_ticket(connection, user)
                        elif booked_choice == '4':
                            show_all_tickets(connection, user)
                        elif booked_choice == '5':
                            break
                        else:
                            error_message("Invalid option. Please enter a valid option.")
                    
                elif option == '3':
                    add_balance(connection, user)
                elif option == '4':
                    view_user_profile(user)
                elif option == '5':
                    update_user_details(connection, user)
                elif option == '6':
                    success_message("Logging out. Goodbye!")
                    break
                else:
                    error_message("Invalid option. Please enter a valid option.")
        elif user and check_password(password, user['password']) and user['status'] == 'BLOCKED':
           full_name = ' '.join(filter(None, [user['first_name'], user['middle_name'], user['last_name']]))
           print("")
           error_message(f'''Dear, {full_name}
Your account has been blocked by our team. We apologize for the inconvenience.
You do not have permission to login. Please contact us via email from your registered email address.''')
           return
    
        else:
            error_message("Invalid credentials. Please try again.")
    except mysql.connector.Error as err:
        error_message(f"Error: {err}")


def main():
    connection = connect_to_database()

    if connection:
        create_train_booking_tables(connection)

        while True:
            try:
                print("")
                print("1. Login")
                print("2. Register")
                print("3. Exit")
                print("")

                choice = input("Enter your choice: ")

                if choice == '1':
                    login_user(connection)
                elif choice == '2':
                    register_user(connection)
                elif choice == '3':
                    error_message("Exiting the Railways Ticket Booking System. Goodbye!")
                    break
                else:
                    error_message("Invalid choice. Please enter a valid option.")

            except KeyboardInterrupt:
                break
            finally:
                connection.close()

if __name__ == "__main__":
    print("")
    letter_animation()
    progress_bar(duration=3)
    main()
