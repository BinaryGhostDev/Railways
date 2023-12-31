from src.text_color import success_message

def view_user_profile(current_user):
    success_message("\nProfile Details:")
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
    print("")
    print("0. Go Back To Menu")
    print("")

    ch = input("Enter 0 for Move to Menu: ")
    
    if ch == '0':  # Corrected to compare with a string
        return

# Sample usage:
# view_user_profile(current_user)
