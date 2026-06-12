my_database = {}

#==================== Registration ====================
def sign_up(full_name, email, password, role):
    #check if email is already taken
    if email in my_database:
        return "ERROR: This email is already registered!"
    
    #strong password validation
    #check length
    if len(password) < 8:
        return "ERROR: Password must be at least 8 character long"
    
    #check for atlist one number
    is_number = False
    for char in password:
        if char.isdigit():
            is_number = True
    
    if not is_number:
        return "ERROR: Password must contain at least one number"
        
    #save the everything including an 'attempt' tracker set to 0 
    my_database[email] = {
        "full_name": full_name,
        "password_hash": password,
        "role": role,
        "attempts": 0  #start at 0 failed attempts
    }
    return "SUCCESS: Account created successfully"

#====================== Login =========================
def log_in(email, password):
    #check if email exists
    if email not in my_database:
        return "ERROR: Email not found!"
    
    #get the data from database
    user_data = my_database[email]
    
    #check if account lock out
    if user_data["attempts"] > 3:
        return "ERROR: To many attempts"
    
    correct_password = user_data["password_hash"]
    role = user_data["role"]

    #check if the password matches the store pasword exactly
    if password == correct_password:
        #reset attempt back to 0 on successful login
        user_data["attempts"] = 0
        return f"SUCCESSFUL: Logg in! Loading the {role} dashboard."
    else:
        #if wrong password increase faoled attempts by 1
        user_data["attempts"] = user_data["attempts"] + 1
        remaining_attempts = 3 - user_data["attempts"]

        if user_data["attempts"] >= 3:
            return "ERROR: Wrong Password. Account is now locked!"
        else:
            return f"ERROR: Wrong Password. You have {remaining_attempts} attempts remaining."

    
 
