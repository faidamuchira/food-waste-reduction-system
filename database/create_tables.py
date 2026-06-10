from db_connection import get_db_connection

# Establish connection to food_waste_db
connection = get_db_connection()

try:
    #check the connection
    if connection.is_connected():
        print("Successful connection to the database")
        
    # create cursor to allow python to execute SQL statements
    cursor = connection.cursor()
    
    # The users table stores both businesses and customers.
    # User roles are used to control access to different features.
    users_table_query = """
    CREATE TABLE IF NOT EXISTS users(
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        full_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL, -- must be unique to prevent duplicate accounts
        password_hash VARCHAR(255) NOT NULL,
        
        -- Restrict role values to valid user types
        role ENUM ('business', 'customer') NOT NULL,
        
        -- Automatically records when the account was created 
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(users_table_query)
    
    print("Users table created successfully")
    

except Exception as e:
    print("Error:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")