import mysql.connector
from prettytable import PrettyTable
from datetime import datetime, timedelta
from src.text_color import success_message, error_message

def display_ticket_details(ticket):
    print("")
    print(f"PNR: {ticket['PNR']} | Passenger Name: {ticket['passenger_name']}")
    print(f"Train Name: {ticket['train_name']}")
    print(f"Boarding To Destination: {ticket['boarding_station_code']} => {ticket['destination_station_code']}")
    print(f"Departure: {ticket['Departure']} => Arrival: {ticket['Arrival']}")
    print(f"Journey Date: {ticket['journey_date']}")
    print(f"Coach: {ticket['seat_class']}, Seat: {ticket['seat']}")
    print(f"Fare: ₹{ticket['fare']}")
    print(f"Booking DateTime: {ticket['booked_time']}")
    # print(f"Status: {ticket['status']}")

def display_ticket_details_pretty(table, booked_ticket):
    route_info = f"{booked_ticket['boarding_station_code']} => {booked_ticket['destination_station_code']}"
    table.add_row([
        booked_ticket['PNR'],
        booked_ticket['train_name'],
        booked_ticket['passenger_name'],
        booked_ticket['Departure'],
        route_info,
        booked_ticket['Arrival'],
        f"{booked_ticket['seat_class']}, Seat: {booked_ticket['seat']}",
        f"₹{booked_ticket['fare']}",
        booked_ticket['journey_date'],
        booked_ticket['booked_time'],
        booked_ticket['status']
    ])


def search_booked_ticket_by_pnr(connection, cursor):
    try:
        cursor = connection.cursor(dictionary=True)

        # Ask the user for PNR number
        pnr_number = input("Enter PNR number: ")

        # Fetch booked ticket details
        cursor.execute("""
            SELECT * FROM bookings
            WHERE PNR = %s
        """, (pnr_number,))

        #print(cursor.statement) #For debugging purposes only

        booked_ticket = cursor.fetchone()
        #print(booked_ticket) # This code write for debugging

        if not booked_ticket:
            error_message("No booked ticket found with the given PNR.")
        else:
            # Check if the ticket has been canceled
            if booked_ticket['status'] == 'CANCELED':
                success_message("\nBooked Ticket Details:")
                display_ticket_details(booked_ticket)
                error_message("Status: Canceled")
            else:
                # Check the current date and journey date
                current_date = datetime.now().date()
                journey_date = booked_ticket['journey_date']

                # Check if the journey date is in the future or the current and journey dates are the same
                if current_date <= journey_date <= current_date + timedelta(days=1):
                    # Check the departure time
                    departure_time = datetime.strptime(str(booked_ticket['Departure']), "%H:%M:%S").time()
                    arrival_time = datetime.strptime(str(booked_ticket['Arrival']), "%H:%M:%S").time()
                    current_time = datetime.now().time()

                    if current_time >= departure_time and current_time <= arrival_time:
                        # Update the status to 'DEPARTURED'
                        cursor.execute("""
                            UPDATE bookings
                            SET status = 'DEPARTURED'
                            WHERE PNR = %s
                        """, (pnr_number,))
                        connection.commit()
                        print("\nBooked Ticket Details:")
                        display_ticket_details(booked_ticket)
                        success_message("Status: DEPARTURED")

                    elif current_time >= arrival_time:
                        # Update the status to 'USED'
                        cursor.execute("""
                            UPDATE bookings
                            SET status = 'COMPLETE JOURNEY'
                            WHERE PNR = %s
                        """, (pnr_number,))
                        connection.commit()
                        print("\nBooked Ticket Details:")
                        display_ticket_details(booked_ticket)
                        success_message("Status: COMPLETE JOURNEY")      
                    else:
                        print("\nBooked Ticket Details:")
                        display_ticket_details(booked_ticket)
                        success_message("Status: BOOKED ( Future Ticket)")

                elif current_date > journey_date:
                        # Update the status to 'USED'
                        cursor.execute("""
                            UPDATE bookings
                            SET status = 'COMPLETE JOURNEY'
                            WHERE PNR = %s
                        """, (pnr_number,))
                        connection.commit()
                        print("\nBooked Ticket Details:")
                        display_ticket_details(booked_ticket)
                        success_message("Status: COMPLETE JOURNEY") 

                elif current_date < journey_date:
                    print("\nBooked Ticket Details:")
                    display_ticket_details(booked_ticket)
                    success_message("Status: BOOKED ( Future Ticket)") 


    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")
        
    except mysql.connector.Error as err:
        error_message(f"Error: {err}")

    finally:
        cursor.close()


def show_all_booked_tickets(connection, cursor):
    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch all booked tickets for the current user
        cursor.execute("""
            SELECT PNR, train_name, passenger_name, Departure, boarding_station_code, destination_station_code, Arrival, seat_class, seat, fare, journey_date, booked_time, status
            FROM bookings
            WHERE status = %s
        """, ('BOOKED',))

        booked_tickets = cursor.fetchall()

        if not booked_tickets:
            error_message("No booked tickets found.")
        else:
            table = PrettyTable()
            table.field_names = ["PNR", "Train Name", "passenger_name", "Departure", "Route", "Arrival", "Seat", "Fare", "Journey Date", "Booking Time", "Status"]

            for booked_ticket in booked_tickets:
                # Check if the ticket has been canceled
                if booked_ticket['status'] == 'CANCELED':
                    # Display ticket details
                    display_ticket_details_pretty(table, booked_ticket)
                else:
                    # Check the current date and journey date
                    current_date = datetime.now().date()
                    journey_date = booked_ticket['journey_date']

                    # Check if the journey date is in the future or the current and journey dates are the same
                    if current_date <= journey_date <= current_date + timedelta(days=1):
                        # Check the departure time
                        departure_time = datetime.strptime(str(booked_ticket['Departure']), "%H:%M:%S").time()
                        arrival_time = datetime.strptime(str(booked_ticket['Arrival']), "%H:%M:%S").time()
                        current_time = datetime.now().time()

                        if current_time >= departure_time and current_time <= arrival_time:
                            # Update the status to 'DEPARTURED'
                            cursor.execute("""
                                UPDATE bookings
                                SET status = 'DEPARTURED'
                                WHERE PNR = %s
                            """, (booked_ticket['PNR'],))
                            connection.commit()

                        elif current_time >= arrival_time:
                            # Update the status to 'COMPLETE JOURNEY'
                            cursor.execute("""
                                UPDATE bookings
                                SET status = 'COMPLETE JOURNEY'
                                WHERE PNR = %s
                            """, (booked_ticket['PNR'],))
                            connection.commit()
                        else:
                            # Display ticket details
                            display_ticket_details_pretty(table, booked_ticket)
                    
                    elif current_date > journey_date:
                            # Update the status to 'COMPLETE JOURNEY'
                            cursor.execute("""
                                UPDATE bookings
                                SET status = 'COMPLETE JOURNEY'
                                WHERE PNR = %s
                            """, (booked_ticket['PNR'],))
                            connection.commit()

                    elif current_date < journey_date:
                        display_ticket_details_pretty(table, booked_ticket)


            # Print the table after the loop
            print("")
            success_message(" Your All Booked Tickets: ")
            print("")
            print(table)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")
    finally:
        cursor.close()


def show_all_tickets(connection, cursor):
    try:
        cursor = connection.cursor(dictionary=True)

        user_id = int(input('Enter user ID: '))

        # Fetch all booked tickets for the current user
        cursor.execute("""
            SELECT PNR, train_name, passenger_name, Departure, boarding_station_code, destination_station_code, Arrival, seat_class, seat, fare, journey_date, booked_time, status
            FROM bookings
            WHERE booked_user_id = %s
        """, (user_id,))

        booked_tickets = cursor.fetchall()

        if not booked_tickets:
            error_message(f"No booked tickets found for user with ID {user_id}.")
        else:
            table = PrettyTable()
            table.field_names = ["PNR", "Train Name", "passenger_name", "Departure", "Route", "Arrival", "Seat", "Fare", "Journey Date", "Booking Time", "Status"]

            for booked_ticket in booked_tickets:
                # Check if the ticket has been canceled
                if booked_ticket['status'] == 'CANCELED':
                    # Display ticket details
                    display_ticket_details_pretty(table, booked_ticket)
                else:
                    # Check the current date and journey date
                    current_date = datetime.now().date()
                    journey_date = booked_ticket['journey_date']

                    # Check if the journey date is in the future or the current and journey dates are the same
                    if current_date <= journey_date <= current_date + timedelta(days=1):
                        # Check the departure time
                        departure_time = datetime.strptime(str(booked_ticket['Departure']), "%H:%M:%S").time()
                        arrival_time = datetime.strptime(str(booked_ticket['Arrival']), "%H:%M:%S").time()
                        current_time = datetime.now().time()

                        if current_time >= departure_time and current_time <= arrival_time:
                            # Update the status to 'DEPARTURED'
                            cursor.execute("""
                                UPDATE bookings
                                SET status = 'DEPARTURED'
                                WHERE PNR = %s
                            """, (booked_ticket['PNR'],))
                            connection.commit()

                        elif current_time >= arrival_time:
                            # Update the status to 'COMPLETE JOURNEY'
                            cursor.execute("""
                                UPDATE bookings
                                SET status = 'COMPLETE JOURNEY'
                                WHERE PNR = %s
                            """, (booked_ticket['PNR'],))
                            connection.commit()

                    elif current_date > journey_date:
                        # Update the status to 'COMPLETE JOURNEY'
                        cursor.execute("""
                            UPDATE bookings
                            SET status = 'COMPLETE JOURNEY'
                            WHERE PNR = %s
                        """, (booked_ticket['PNR'],))
                        connection.commit()

                    elif current_date < journey_date:
                        display_ticket_details_pretty(table, booked_ticket) 

            # Print the table after the loop
            print("")
            success_message(f" Your All Tickets Found as per your given USER ID {user_id} : ")
            print("")
            print(table)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()


def cancel_booked_ticket(connection, cursor):
    try:
        # Ask the user for the PNR number to cancel
        pnr = input("Enter the PNR number of the ticket you want to cancel: ")

        cursor = connection.cursor(dictionary=True)

        # Fetch the booked ticket details
        cursor.execute("""
            SELECT booked_user_id, PNR, train_name, passenger_name, Departure, Arrival, seat_class, seat, fare, journey_date, status
            FROM bookings
            WHERE PNR = %s
        """, (pnr,))

        booked_ticket = cursor.fetchone()

        debit_fare = booked_ticket['fare'] * 10/100
        final_fare_added = booked_ticket['fare'] - debit_fare

        if not booked_ticket:
            error_message("No booked ticket found with the provided PNR.")
        else:
            # Check if the ticket has already been canceled
            if booked_ticket['status'] == 'CANCELED':
                print("")
                error_message("This ticket has already been canceled.")
            else:
                # Check the current date and journey date
                current_date = datetime.now().date()
                journey_date = booked_ticket['journey_date']

                # Check if the journey date is in the future or the current and journey dates are the same
                if current_date <= journey_date <= current_date + timedelta(days=1):
                    # Check the departure time
                    departure_time = datetime.strptime(str(booked_ticket['Departure']), "%H:%M:%S").time()
                    arrival_time = datetime.strptime(str(booked_ticket['Arrival']), "%H:%M:%S").time()
                    current_time = datetime.now().time()

                    if current_time >= departure_time and current_time <= arrival_time:
                        # Update the status to 'CANCELED'
                        cursor.execute("""
                            UPDATE bookings
                            SET status = 'CANCELED'
                            WHERE PNR = %s
                        """, (pnr,))

                        # Update the user's wallet by adding the fare
                        cursor.execute("""
                            UPDATE users
                            SET wallet = wallet + %s
                            WHERE id = %s
                        """, (final_fare_added, booked_ticket['booked_user_id']))
                            
                        connection.commit()
                        # Display ticket details after cancellation
                        success_message(f"Ticket successfully canceled. And Refund Added Successfully to User Wallet.")

                    elif current_time >= arrival_time:
                        # Update the status to 'COMPLETE JOURNEY'
                        cursor.execute("""
                            UPDATE bookings
                            SET status = 'COMPLETE JOURNEY'
                            WHERE PNR = %s
                        """, (booked_ticket['PNR'],))
                        connection.commit()
                        print("")
                        error_message("This Train is Arrived You can't Cancel this Train Ticket")
                    else:
                        # Update the status to 'CANCELED'
                        cursor.execute("""
                            UPDATE bookings
                            SET status = 'CANCELED'
                            WHERE PNR = %s
                        """, (pnr,))

                        # Update the user's wallet by adding the fare
                        cursor.execute("""
                            UPDATE users
                            SET wallet = wallet + %s
                            WHERE id = %s
                        """, (final_fare_added, booked_ticket['booked_user_id']))

                        connection.commit()
                        # Display ticket details after cancellation
                        success_message(f"Ticket successfully canceled. And Refund Added Successfully to User Wallet.")
                
                else:
                     # Update the status to 'CANCELED'
                    cursor.execute("""
                     UPDATE bookings
                     SET status = 'CANCELED'
                    WHERE PNR = %s
                    """, (pnr,))

                    # Update the user's wallet by adding the fare
                    cursor.execute("""
                     UPDATE users
                     SET wallet = wallet + %s
                     WHERE id = %s
                     """, (final_fare_added, booked_ticket['booked_user_id']))
                    
                    connection.commit()
                    # Display ticket details after cancellation
                    success_message(f"Ticket successfully canceled. And Refund Added Successfully to User Wallet.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")
    finally:
        cursor.close()


def Manage_Booked_Tickets(connection, cursor):

    try:
            
        while True:
            print("\nManage Booked Tickets Menu:")
            print("1. Search Ticket By PNR")
            print("2. Show all Booked Tickets")
            print("3. Cancel Ticket By PNR")
            print("4. Show All Tickets By User Id")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                search_booked_ticket_by_pnr(connection, cursor)
            elif choice == '2':
                show_all_booked_tickets(connection, cursor)
            elif choice == '3':
                cancel_booked_ticket(connection, cursor)
            elif choice == '4':
                show_all_tickets(connection, cursor)
            elif choice == '5':
                success_message("Exiting Manage Booked Tickets menu.")
                break
            else:
                error_message("Invalid choice. Please enter a valid option.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

# Sample usage:
# ticket = {'PNR': '123456', 'train_name': 'Express', 'Departure': '10:00:00', 'Arrival': '12:00:00', 'journey_date': '2023-12-30', 'seat_class': 'SL', 'seat': 'A1', 'fare': 500, 'booking_datetime': '2023-12-29 08:30:00', 'status': 'BOOKED'}
# display_ticket_details(ticket)
