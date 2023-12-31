import os
from src.text_color import error_message

def main():
    print("Welcome to the Railways Ticketing System")
    print("")
    print("Are you an admin or a user?")
    
    try:

        while True:
            role = input("Enter 'admin' or 'user': ").lower()

            if role == 'admin':
                os.system("python admin.py")
                break
            elif role == 'user':
                os.system("python user.py")
                break
            else:
                print("Invalid input. Please enter 'admin' or 'user'.")
    except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C)
     error_message("\n\nExiting due to user interruption. Goodbye!")

main()
