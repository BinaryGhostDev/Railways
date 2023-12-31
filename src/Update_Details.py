import mysql.connector
from src.text_color import success_message, error_message

def update_user_details(connection, current_user):
    try:
        cursor = connection.cursor()

        # Display current user details
        display_current_user_details(current_user)

        # Ask the user which details to update
        print("\nSelect the details you want to update:")
        print("1.  Password")
        print("2.  First Name")
        print("3.  Middle Name")
        print("4.  Last Name")
        print("5.  Occupation")
        print("6.  Country")
        print("7.  Gender")
        print("8.  Email")
        print("9.  Mobile Number")
        print("10. Address")
        print("0.  Exit")

        choice = int(input("Enter your choice (0-10): "))

        if choice == 0:
            success_message("Exiting update process.")
        else:
            # Get the new value for the selected detail
            new_value = input(f"Enter the new value for {get_column_name(choice)}: ")

            # Update the user details in the database
            update_user_detail(connection, current_user, choice, new_value)

    except ValueError:
        error_message("Invalid input. Please enter a valid numeric value.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")
        
    except mysql.connector.Error as err:
        error_message(f"Database error: {err}")

    finally:
        cursor.close()

def display_current_user_details(current_user):
    print("\nCurrent User Details:")
    print("")
    print("Username:", current_user['username'])
    print("Password: [HIDDEN]")
    print("First Name:", current_user['first_name'])
    print("Middle Name:", current_user['middle_name'])
    print("Last Name:", current_user['last_name'])
    print("Occupation:", current_user['occupation'])
    print("Country:", current_user['country'])
    print("Gender:", current_user['gender'])
    print("Email:", current_user['email'])
    print("Mobile Number:", current_user['mobile_number'])
    print("Address:", current_user['address'])

def get_column_name(choice):
    # Map the choice to the corresponding column name
    column_names = {
        1: 'password',
        2: 'first_name',
        3: 'middle_name',
        4: 'last_name',
        5: 'occupation',
        6: 'country',
        7: 'gender',
        8: 'email',
        9: 'mobile_number',
        10: 'address'
    }
    return column_names.get(choice, '')

def update_user_detail(connection, current_user, choice, new_value):
    try:
        cursor = connection.cursor()

        # Get the column name for the selected choice
        column_name = get_column_name(choice)

        # Update the user details in the database
        cursor.execute(f"""
            UPDATE users
            SET {column_name} = %s
            WHERE id = %s
        """, (new_value, current_user['id']))

        connection.commit()
        success_message("User details updated successfully.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except mysql.connector.Error as err:
        error_message(f"Error updating user details: {err}")

    finally:
        cursor.close()

# Sample usage:
# update_user_details(connection, current_user)
