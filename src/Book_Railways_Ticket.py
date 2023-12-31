import random
import mysql.connector
from prettytable import PrettyTable
from src.text_color import success_message, error_message
from datetime import datetime, timedelta

# Assuming you have a function connect_to_database() to establish the database connection

def get_current_seat_availability(cursor, train_id, coach_class, journey_date):
    cursor.execute(f"SELECT `{coach_class} Seats` FROM trains WHERE `id` = %s", (train_id,))
    total_seats = cursor.fetchone()[f"{coach_class} Seats"]

    cursor.execute("""
        SELECT COUNT(`booking_id`) as total_booked_seats
        FROM bookings
        WHERE `train_id` = %s AND `seat_class` = %s AND `journey_date` = %s AND `status` = %s
    """, (train_id, coach_class, journey_date, 'BOOKED'))

    total_booked_seats = cursor.fetchone()['total_booked_seats']
    available_seats = total_seats - total_booked_seats

    return available_seats

def display_seat_availability_with_price_and_bookings(cursor, train, journey_date):
    success_message("\nSeat Availability:")
    print("")
    print(f"SL Seats: {get_current_seat_availability(cursor, train['id'], 'SL', journey_date)}, Fare: {train['SL Fare']}")
    print(f"1A Seats: {get_current_seat_availability(cursor, train['id'], '1A', journey_date)}, Fare: {train['1A Fare']}")
    print(f"2A Seats: {get_current_seat_availability(cursor, train['id'], '2A', journey_date)}, Fare: {train['2A Fare']}")
    print(f"3A Seats: {get_current_seat_availability(cursor, train['id'], '3A', journey_date)}, Fare: {train['3A Fare']}")

def book_railways_ticket(connection, current_user):
    try:
        cursor = connection.cursor(dictionary=True)

        # Ask user for boarding and destination station codes
        boarding_station_code = input("Enter Boarding Station Code: ")
        destination_station_code = input("Enter Destination Station Code: ")

        # Check if the route exists in the database
        cursor.execute("""
            SELECT id, train_name, boarding_station_code, destination_station_code, Departure, Arrival, `SL Fare`, `1A Fare`, `2A Fare`, `3A Fare`,
                `SL Seats`, `1A Seats`, `2A Seats`, `3A Seats`
            FROM trains
            WHERE boarding_station_code = %s AND destination_station_code = %s
        """, (boarding_station_code, destination_station_code))

        trains = cursor.fetchall()

        if not trains:
            error_message("No trains found for the given route.")
            return

        # Display available trains in a table
        table = PrettyTable()
        table.field_names = ["#", "Train Name", "Boarding => Destination", "Departure Time", "Arrival Time", "SL Seats", "1A Seats", "2A Seats", "3A Seats"]

        for i, train in enumerate(trains, start=1):
            route_info = f"{train['boarding_station_code']} => {train['destination_station_code']}"
            table.add_row([i, train['train_name'], route_info, train['Departure'], train['Arrival'], train['SL Seats'], train['1A Seats'], train['2A Seats'], train['3A Seats']])

        print(table)

        while True:
            # Ask user to choose a train
            choice = int(input("Enter the number of the train you want to book: "))

            if choice < 1 or choice > len(trains):
                error_message("Invalid choice. Please enter a valid train number.")
                continue

            selected_train = trains[choice - 1]

            current_date = datetime.now().date()

            # Ask user for the journey date
            journey_date_str = input("Enter Journey Date (YYYY-MM-DD): ")
            journey_date = datetime.strptime(journey_date_str, "%Y-%m-%d").date()

            if journey_date == current_date:
                error_message("Invalid journey date. You cannot book a ticket for today's date.")
                print("")
                continue
            elif journey_date == current_date + timedelta(days=1):
                error_message("Invalid journey date. You cannot book a ticket for tomorrow date.")
                print("")
                continue
            else:
                pass

            # Display seat availability information for the selected date
            display_seat_availability_with_price_and_bookings(cursor, selected_train, journey_date)
            print("")
            print("4. Change the train")
            print("0. Go back menu")
            print("")

            # Ask user to choose a coach class
            coach_class = input("Choose Coach Class (SL, 1A, 2A, 3A): ").upper()
            if coach_class == '4':
                continue
            elif coach_class == '0':
                break
            else:
                pass

            while True:
                # Get total number of seats based on the chosen coach class
                total_seats = selected_train[f"{coach_class} Seats"]

                # Check if seat is available for the selected train and date
                # Generate a random seat number based on the total number of seats for the selected class
                seat = random.randint(1, total_seats)

                # Check if the seat is already booked for the selected train, date, and coach class
                cursor.execute("""
                    SELECT COUNT(`booking_id`) as seat_count
                    FROM bookings
                    WHERE `train_id` = %s AND `seat_class` = %s
                    AND `seat` = %s AND `journey_date` = %s AND `status` = %s
                """, (selected_train['id'], coach_class, seat, journey_date, 'BOOKED'))

                seat_count = cursor.fetchone()['seat_count']

                if seat_count == 0:
                    # Exit the loop if the seat is available
                    break
                else:
                    break

            # Get user's wallet balance
            cursor.execute("SELECT wallet FROM users WHERE `id` = %s", (current_user['id'],))
            user = cursor.fetchone()

            if not user:
                error_message("User not found.")
                return

            wallet_balance = user['wallet']
            fare = selected_train[f"{coach_class} Fare"]

            # Check if user has sufficient balance
            if wallet_balance < fare:
                error_message(f"Insufficient balance. Please add balance to your wallet.")
                return

            # Deduct fare from the user's wallet
            cursor.execute("UPDATE users SET wallet = wallet - %s WHERE `id` = %s", (fare, current_user['id']))
            connection.commit()

            # Ask for passenger details
            passenger_name = input("Enter Passenger Name: ")
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")
            aadhar_number = input("Enter Aadhar Number: ")
            mobile_number = input("Enter Mobile Number: ")

            pnr = random.randint(1000000, 9999999)
            status ="BOOKED"

            # Insert booking details into the bookings table
            cursor.execute("""
                INSERT INTO bookings (
                    booked_username,
                    booked_user_id,
                    train_id,
                    PNR,
                    train_name,
                    passenger_name,
                    dob,
                    aadhar_number,
                    mobile_number,
                    boarding_station_code,
                    destination_station_code,
                    seat_class,
                    seat,
                    fare,
                    payment_status,
                    journey_date,
                    `status`,
                    Departure,
                    Arrival,
                    booked_time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                current_user['username'],
                current_user['id'],
                selected_train['id'],
                pnr,
                selected_train['train_name'],
                passenger_name,
                dob,
                aadhar_number,
                mobile_number,
                boarding_station_code,
                destination_station_code,
                coach_class,
                seat,
                fare,
                'Verified',
                journey_date,
                status,
                selected_train['Departure'],
                selected_train['Arrival'],
                datetime.now()
            ))

            connection.commit()

            print("")
            success_message(f"Ticket booked successfully for {selected_train['train_name']}!")
            print("")
            success_message(f"PNR: {pnr} | Passenger Name: {passenger_name}")
            print("Boarding To Destination:", boarding_station_code, "=>", destination_station_code, f"| Passenger Journey: {journey_date}")
            print(f"Train Departure Time => {selected_train['Departure']} Train Arrival Time => {selected_train['Arrival']}")
            print(f"Coach: {coach_class}, Seat: {seat}")
            print("")
            print("Current Status: ", status)

            break  # Exit the loop if the booking is successful

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")
        
    except mysql.connector.Error as err:
        error_message(f"Error: {err}")

    finally:
        cursor.close()

# Example of how to call the function
# Make sure to replace `connection` and `current_user` with your actual connection and user data
# book_railways_ticket(connection, current_user)
