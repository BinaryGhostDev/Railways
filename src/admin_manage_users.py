from prettytable import PrettyTable
from src.text_color import success_message, error_message

def show_all_users(cursor):
    try:
        # Fetch all users from the users table
        cursor.execute("""
            SELECT id, first_name, last_name, occupation, country, mobile_number, email, status
            FROM users
        """)

        users = cursor.fetchall()

        if not users:
            error_message("No users found.")
        else:
            table = PrettyTable()
            table.field_names = ["ID", "First Name", "Last Name", "Occupation", "Country", "Mobile Number", "Email", "Status"]

            for user in users:
                # Check if the tuple has at least 8 elements
                if len(user) >= 8:
                    table.add_row([user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7]])
                else:
                    error_message(f"Error: Tuple length is less than expected. Tuple: {user}")

            # Print the table
            print("")
            success_message(" All Users:")
            print("")
            print(table)


    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")


def credit_balance(cursor, connection):
    try:
        while True:
            user_id = input("Enter user ID (Enter 0 to break): ")

            if user_id == '0':
                print("Breaking the process.")
                break

            user_id = int(user_id)

            # Fetch user details before asking for the credit amount
            cursor.execute("""
                SELECT id, first_name, last_name, mobile_number, wallet
                FROM users
                WHERE id = %s
            """, (user_id,))

            user_before = cursor.fetchone()

            if not user_before:
                error_message("No user found with the provided ID.")
                continue

            # Display user details before crediting in a table
            table_before = PrettyTable()
            table_before.field_names = ["ID", "First Name", "Last Name", "Mobile Number", "Wallet Balance"]
            table_before.add_row([user_before[0], user_before[1], user_before[2], user_before[3], user_before[4]])

            print("\nUser Details Before Credit:")
            print(table_before)

            amount = float(input("Enter the amount to credit: "))

            # Update the user's wallet by adding the amount
            cursor.execute("""
                UPDATE users
                SET wallet = wallet + %s
                WHERE id = %s
            """, (amount, user_id))

            connection.commit()
            print("")
            success_message("Balance credited successfully.")

            # Fetch user details after updating the wallet balance
            cursor.execute("""
                SELECT id, first_name, last_name, wallet
                FROM users
                WHERE id = %s
            """, (user_id,))

            user_after = cursor.fetchone()

            if user_after:
                # Display user details after crediting in a success message
                success_message(f"User ID: {user_after[0]}, Name: {user_after[1]} {user_after[2]}, Wallet Balance: {user_after[3]}")
            else:
                print("")
                error_message("No user found with the provided ID after credit.")
                print("")

            break_prompt = input("Do you want to process another user? (yes/no): ").lower()
            if break_prompt != 'yes' and break_prompt != 'y':
                print("Breaking the process.")
                break
    
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")


def debit_balance(cursor, connection):
    try:
        while True:
            user_id = input("Enter user ID (Enter 0 to break): ")

            if user_id == '0':
                print("Breaking the process.")
                break

            user_id = int(user_id)

            # Fetch user details before asking for the debit amount
            cursor.execute("""
                SELECT id, first_name, last_name, mobile_number, wallet
                FROM users
                WHERE id = %s
            """, (user_id,))

            user_before = cursor.fetchone()

            if not user_before:
                error_message("No user found with the provided ID.")
                continue

            # Display user details before debiting in a table
            table_before = PrettyTable()
            table_before.field_names = ["ID", "First Name", "Last Name", "Mobile Number", "Wallet Balance"]
            table_before.add_row([user_before[0], user_before[1], user_before[2], user_before[3], user_before[4]])

            print("\nUser Details Before Debit:")
            print(table_before)

            amount = float(input("Enter the amount to debit: "))

            # Update the user's wallet by subtracting the amount
            cursor.execute("""
                UPDATE users
                SET wallet = wallet - %s
                WHERE id = %s
            """, (amount, user_id))

            connection.commit()
            print("")
            success_message("Balance debited successfully.")

            # Fetch user details after updating the wallet balance
            cursor.execute("""
                SELECT id, first_name, last_name, wallet
                FROM users
                WHERE id = %s
            """, (user_id,))

            user_after = cursor.fetchone()

            if user_after:
                # Display user details after debiting in a success message
                success_message(f"User ID: {user_after[0]}, Name: {user_after[1]} {user_after[2]}, Wallet Balance: {user_after[3]}")
            else:
                print("")
                error_message("No user found with the provided ID after debit.")
                print("")

            break_prompt = input("Do you want to process another user? (yes/no): ").lower()
            if break_prompt != 'yes' and break_prompt != 'y':
                print("Breaking the process.")
                break
    
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")



def block_user(cursor, connection):
    try:
        user_id = int(input("Enter user ID to block: "))

        # Fetch user details before blocking
        cursor.execute("""
            SELECT id, first_name, last_name, occupation, country, mobile_number, email, status
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            error_message("No user found with the provided ID.")
            return

        # Display user details before blocking
        table = PrettyTable()
        table.field_names = ["ID", "First Name", "Last Name", "Occupation", "Country", "Mobile Number", "Email", "Status"]
        table.add_row([user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7]])
        print("\nUser Details Before Blocking:")
        print(table)

        # Confirm if the user should be blocked
        confirmation = input(f"Do you want to block user {user[0]} ({user[1]} {user[2]})? (yes/no): ").lower()

        if confirmation == 'yes' or confirmation == 'y':
            # Update user status to 'BLOCKED'
            cursor.execute("""
                UPDATE users
                SET status = 'BLOCKED'
                WHERE id = %s
            """, (user_id,))
            connection.commit()
            success_message(f"User {user[0]} ({user[1]} {user[2]}) has been blocked.")
        else:
            print("Blocking operation cancelled.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")
        
    except Exception as e:
        error_message(f"Error: {e}")


def unblock_user(cursor, connection):
    try:
        user_id = int(input("Enter user ID to unblock: "))

        # Fetch user details before unblocking
        cursor.execute("""
            SELECT id, first_name, last_name, occupation, country, mobile_number, email, status
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            error_message("No user found with the provided ID.")
            return

        # Display user details before unblocking
        table = PrettyTable()
        table.field_names = ["ID", "First Name", "Last Name", "Occupation", "Country", "Mobile Number", "Email", "Status"]
        
        # Add user details to the table
        table.add_row([user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7]])

        error_message("\nUser Details Before Unblocking:")
        print(table)

        # Confirm if the user should be unblocked
        confirmation = input(f"Do you want to unblock user {user[0]} ({user[1]} {user[2]})? (yes/no): ").lower()

        if confirmation == 'yes' or confirmation == 'y':
            # Update user status to 'ACTIVE'
            cursor.execute("""
                UPDATE users
                SET status = 'ACTIVE'
                WHERE id = %s
            """, (user_id,))
            connection.commit()
            success_message(f"User {user[0]} ({user[1]} {user[2]}) has been unblocked.")
        else:
            error_message("Unblocking operation cancelled.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")


def manage_users_menu(connection, cursor):
    try:
            
        while True:
            print("\nManage Users Menu:")
            print("")
            print("1. Show All Users")
            print("2. Debit Balance")
            print("3. Credit Balance")
            print("4. Block User")
            print("5. Unblock User")
            print("6. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                show_all_users(cursor)
            elif choice == '2':
                debit_balance(cursor, connection)
            elif choice == '3':
                credit_balance(cursor, connection)
            elif choice == '4':
                block_user(cursor, connection)
            elif choice == '5':
                unblock_user(cursor, connection)
            elif choice == '6':
                print("Exiting Manage Users. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
    
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

# Sample usage:
# manage_users_menu(connection, cursor)
