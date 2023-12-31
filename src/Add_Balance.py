import mysql.connector
from datetime import datetime
from src.text_color import success_message, error_message

def add_balance(connection, current_user):
    try:
        cursor = connection.cursor()

        # Ask the user for the balance to add
        balance_amount = float(input("Enter the balance amount to add: "))

        # Ask the user for the payment method
        payment_method = int(input("Choose a payment method:\n1. UPI Payment Gateway\n2. Bank Transfer\nEnter your choice: "))

        if payment_method == 1:
            transaction_id = input("Enter 12-digit Transaction ID: ")

            # Process payment
            process_payment(connection, current_user, transaction_id, balance_amount)

        elif payment_method == 2:
            print("")
            print("BANK NAME: STATE BANK OF INDIA")
            print("ACCOUNT NAME: RAJAN GOSWAMI")
            print("ACCOUNT NUMBER: 258545285245")
            print("IFSC CODE: SBI000082")
            print("")
            success_message("Send the payment above account details then fill the transaction details")
            print("")
            transaction_id = input("Enter 12-digit Transaction ID: ")

            # Process payment
            process_payment(connection, current_user, transaction_id, balance_amount)

        else:
            error_message("Invalid choice. Please choose a valid payment method.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")
        
    except ValueError:
        error_message("Invalid input. Please enter a valid numeric value for the balance.")

    except mysql.connector.Error as err:
        error_message(f"Database error: {err}")

    finally:
        cursor.close()

def process_payment(connection, current_user, transaction_id, balance_amount):
    try:
        # Here, you can add logic to validate the payment and transaction ID
        # For simplicity, let's assume the payment is successful

        # Insert the transaction details into the database
        insert_transaction_into_database(connection, current_user, transaction_id, balance_amount)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except Exception as e:
        error_message(f"Error processing payment: {e}")

def insert_transaction_into_database(connection, current_user, transaction_id, balance_amount):
    try:
        cursor = connection.cursor()

        # Insert transaction details into the database
        cursor.execute("""
            INSERT INTO transactions (user_id, transaction_id, amount, status)
            VALUES (%s, %s, %s, %s)
        """, (current_user['id'], transaction_id, balance_amount, 'PENDING'))

        connection.commit()
        success_message("Transaction details added successfully. Your balance will be updated once the payment is verified.")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C)
        error_message("\n\nExiting due to user interruption. Goodbye!")

    except mysql.connector.Error as err:
        error_message(f"Error inserting transaction details into the database: {err}")

    finally:
        cursor.close()

# Sample usage:
# add_balance(connection, current_user)
