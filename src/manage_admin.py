from prettytable import PrettyTable
from src.text_color import success_message, error_message

def show_all_admins(cursor):
    try:
        # Fetch all admins from the admin table
        cursor.execute("""
            SELECT id, username, full_name, status
            FROM admin
        """)

        admins = cursor.fetchall()

        if not admins:
            error_message("No admins found.")
        else:
            table = PrettyTable()
            table.field_names = ["ID", "Username", "Full Name", "Status"]

            for admin in admins:
                # Check if the tuple has at least 4 elements
                if len(admin) >= 4:
                    table.add_row([admin[0], admin[1], admin[2], admin[3]])
                else:
                    error_message(f"Error: Tuple length is less than expected. Tuple: {admin}")

            # Print the table
            print("")
            success_message(" All Admins:")
            print("")
            print(table)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")

def block_admin(cursor, connection):
    try:
        admin_id = int(input("Enter admin ID to block: "))

        # Fetch admin details before blocking
        cursor.execute("""
            SELECT id, username, full_name, status
            FROM admin
            WHERE id = %s
        """, (admin_id,))

        admin = cursor.fetchone()

        if not admin:
            error_message("No admin found with the provided ID.")
            return

        # Display admin details before blocking
        table = PrettyTable()
        table.field_names = ["ID", "Username", "Full Name", "Status"]
        table.add_row([admin[0], admin[1], admin[2], admin[3]])
        print("\nAdmin Details Before Blocking:")
        print(table)

        # Confirm if the admin should be blocked
        confirmation = input(f"Do you want to block admin {admin[0]} ({admin[1]} {admin[2]})? (yes/no): ").lower()

        if confirmation == 'yes' or confirmation == 'y':
            # Update admin status to 'BLOCKED'
            cursor.execute("""
                UPDATE admin
                SET status = 'BLOCKED'
                WHERE id = %s
            """, (admin_id,))
            connection.commit()
            error_message(f"Admin {admin[0]} ({admin[1]} {admin[2]}) has been blocked.")
        else:
            error_message("Blocking operation cancelled.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")

def unblock_admin(cursor, connection):
    try:
        admin_id = int(input("Enter admin ID to unblock: "))

        # Fetch admin details before unblocking
        cursor.execute("""
            SELECT id, username, full_name, status
            FROM admin
            WHERE id = %s
        """, (admin_id,))

        admin = cursor.fetchone()

        if not admin:
            error_message("No admin found with the provided ID.")
            return

        # Display admin details before unblocking
        table = PrettyTable()
        table.field_names = ["ID", "Username", "Full Name", "Status"]

        # Add admin details to the table
        table.add_row([admin[0], admin[1], admin[2], admin[3]])

        error_message("\nAdmin Details Before Unblocking:")
        print(table)

        # Confirm if the admin should be unblocked
        confirmation = input(f"Do you want to unblock admin {admin[0]} ({admin[1]} {admin[2]})? (yes/no): ").lower()

        if confirmation == 'yes' or confirmation == 'y':
            # Update admin status to 'ACTIVE'
            cursor.execute("""
                UPDATE admin
                SET status = 'ACTIVE'
                WHERE id = %s
            """, (admin_id,))
            connection.commit()
            success_message(f"Admin {admin[0]} ({admin[1]} {admin[2]}) has been unblocked.")
        else:
            error_message("Unblocking operation cancelled.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error: {e}")

def manage_admins_menu(connection, cursor):
    try:
        while True:
            print("\nManage Admins Menu:")
            print("")
            print("1. Show All Admins")
            print("2. Block Admin")
            print("3. Unblock Admin")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                show_all_admins(cursor)
            elif choice == '2':
                block_admin(cursor, connection)
            elif choice == '3':
                unblock_admin(cursor, connection)
            elif choice == '4':
                print("Exiting Manage Admins. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
                
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

# Sample usage:
# manage_admins_menu(connection, cursor)
