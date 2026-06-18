import mysql.connector
from database.db_connection import get_db_connection


#==================== HASH FUNCTION ===================
def hash_function(password: str) -> str:
    #convert plain text password into a unique numeric fingerprint string.
    hash_value = 0
    prime_multiplier = 31 
    modulus = 10**9 + 7

    for char in password:
        #get the unique ASCII code of the character
        hash_value = (hash_value * prime_multiplier + ord(char)) % modulus
    return str(hash_value)


#==================== USER REGISTRATION ====================
def sign_up(full_name, email, password, role):
    #strong password validation
    #check minimum password string length
    if len(password) < 8:
        return False, "ERROR: Password must be at least 8 characters long"
    
    #check for at least one digit involved in password
    is_number = False
    for char in password:
        if char.isdigit():
            is_number = True
    
    if not is_number:
        return False, "ERROR: Password must contain at least one number"
    
    #Scramble the plain text password using our custom rolling function
    scrambled_password = hash_function(password)
        
    # Intialize the databse connection pipes 
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # SQL Command Construction:
        # The '%s' markers act as secure data placeholders. 
        # We explicitly map the tracking number 0 into the hidden 'attempts' column.
        query = """
            INSERT INTO users (full_name, email, password_hash, role, attempts) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (full_name, email, scrambled_password, role, 0)

        # Run the command and issue a database commit to permanently finalize the row
        cursor.execute(query, values)
        connection.commit() # Permanently writes the user profile to your database rows
        return True, "SUCCESS: Account created successfully"

    except mysql.connector.Error as err:
        # MySQL Error 1062 represents a duplicate entry violation for UNIQUE columns
        if err.errno == 1062:
            return False, "ERROR: This Email is already registered!"
        
        #General backup response for unexpected database server faults
        return False,  f"ERROR: Database error: {err.msg}"

    finally:
        #Safely close database connections to prevent memory resource leaks
        cursor.close()
        connection.close()

#====================== USER LOGIN =========================
def log_in(email, password):
    connection = get_db_connection()
    # dictionary=True converts raw tuple rows into easy-to-read Python dictionaries
    cursor = connection.cursor(dictionary=True)

    try:
        # Query data safely using placeholder substitution to prevent SQL injection vulnerabilities
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()

        # Check if user record row was found
        if not user_data:
            return False, "ERROR: Email not found!", None

        # Check if the account lockout flag is active
        if user_data["attempts"] >= 3:
            return False, "ERROR: Too many attempts. Account is locked!", None

        # Extract parameters from the verified data mapping row
        stored_hash = user_data["password_hash"]
        role = user_data["role"]

        # Verify match against our custom polynomial fingerprint
        if hash_function(password) == stored_hash:
            # Reset consecutive failed attempts back to zero on clear authorization
            reset_query = "UPDATE users SET attempts = 0 WHERE email = %s"
            cursor.execute(reset_query, (email,))
            connection.commit()
            return True, f"SUCCESSFUL: Logged in!", user_data
        else:
            # Increment tracking index counter in the user data row
            new_attempts = user_data["attempts"] + 1
            update_query = "UPDATE users SET attempts = %s WHERE email = %s"
            cursor.execute(update_query, (new_attempts, email))
            connection.commit()

            remaining_attempts = 3 - new_attempts

            if new_attempts >= 3:
                return False, "ERROR: Wrong Password. Account is locked!", None 
            else:
                return False, f"ERROR: Wrong Password. You have {remaining_attempts} attempts remaining.", None

    except mysql.connector.Error as err:
        return False, f"ERROR: Database connection error: {err.msg}", None

    finally:
        #Close database operational objects
        cursor.close()
        connection.close()
    

    
 
