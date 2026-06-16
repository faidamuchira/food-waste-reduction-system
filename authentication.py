my_database = {}

#==================== Hash Function ===================
def hash_function(password: str) -> str:
    #convert plain text password into a unique numeric fingerprint string.
    hash_value = 0
    prime_multiplier = 31 
    modulus = 10**9 + 7

    for char in password:
        #get the unique ASCII code of the character
        hash_value = (hash_value * prime_multiplier + ord(char)) % modulus
    return str(hash_value)


#==================== Registration ====================
def sign_up(full_name, email, password, role):
    #check if email is already taken
    if email in my_database:
        return "ERROR: This Email is already registered!"
    
    #strong password validation
    #check length
    if len(password) < 8:
        return "ERROR: Password must be at least 8 characters long"
    
    #check for at least one number
    is_number = False
    for char in password:
        if char.isdigit():
            is_number = True
    
    if not is_number:
        return "ERROR: Password must contain at least one number"
    
    #Scramble the plain text password using our custom match function
    scrambled_password = hash_function(password)
        
    #save the everything including an 'attempt' tracker set to 0 
    my_database[email] = {
        "full_name": full_name,
        "password_hash": scrambled_password, #store safely as a hash fingerprint
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
    if user_data["attempts"] >= 3:
        return "ERROR: Too many attempts. Account is locked!"
    
    stored_hash = user_data["password_hash"]
    role = user_data["role"]

    #check if the password matches the store pasword exactly
    if hash_function(password) == stored_hash:
        #reset attempt back to 0 on successful login
        user_data["attempts"] = 0
        return f"SUCCESSFUL: Logged in! Loading the {role} dashboard."
    else:
        #if wrong password increase faoled attempts by 1
        user_data["attempts"] = user_data["attempts"] + 1
        remaining_attempts = 3 - user_data["attempts"]

        if user_data["attempts"] >= 3:
            return "ERROR: Wrong Password. Account is now locked!"
        else:
            return f"ERROR: Wrong Password. You have {remaining_attempts} attempts remaining."

    
 
