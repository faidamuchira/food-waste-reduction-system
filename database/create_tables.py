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
        attempts INT DEFAULT 0,
        
        -- Automatically records when the account was created 
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP

        
    )
    """
    
    cursor.execute(users_table_query)
    
    # print("Users table created successfully")
    
    # The food_listings table stores surplus food posted by businesses.
    # Customers can browse and reserve these listings before they are discarded.
    food_listings_query = """
    CREATE TABLE IF NOT EXISTS food_listings(
        -- Unique identifier for each listing
        listing_id INT AUTO_INCREMENT PRIMARY KEY,
        
        -- Links the listing to the business that created it
        business_id INT NOT NULL,
        
        food_name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT null,
        quantity INT NOT NULL,
        
         -- Address where customers collect the food
        pickup_address VARCHAR(255),
                   
        -- Coordinates obtained from Google Maps API
        latitude DECIMAL(10,8),
        longitude DECIMAL(11,8),
        
        -- Deadline for reserving or collecting the food
        available_until DATETIME,
        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
         -- Relationship between food listings and businesses
        FOREIGN KEY (business_id) REFERENCES users(user_id)
    )
    
    """
    
    cursor.execute(food_listings_query)
    
    # print("Food listings table created successfully")
    
    # cursor.execute("""
                   
                 #  ALTER TABLE food_listings
                  # -- Address where customers collect the food
                  # ADD pickup_address VARCHAR(255),
                   
                  # -- Coordinates obtained from Google Maps API
                  # ADD latitude DECIMAL(10,8),
                  # ADD longitude DECIMAL(11,8)
                   #""")
    # print("Food listings table altered successfully")
    
    # Store reservations by customers for available food listings
    reservations_table_query = """
    CREATE TABLE IF NOT EXISTS reservations(
        -- Unique identifier for each reservation
        reservation_id INT AUTO_INCREMENT PRIMARY KEY,
        
        -- customer who made the reservation
        customer_id INT NOT NULL,
        
        -- Food listing being reserved
        listing_id INT NOT NULL,
        
        -- Number of items reserved
        quantity_reserved INT NOT NULL,
        
        -- Track the current state of the reservation
        status ENUM('pending', 'collected', 'cancelled') NOT NULL,
        
        -- record the time of reservation
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        -- Relationship between reservations and customers
        FOREIGN KEY (customer_id) REFERENCES users(user_id),
        
        -- Relationship bwteen reservation and food listings
        FOREIGN KEY (listing_id) REFERENCES food_listings(listing_id)
    )
    """
    cursor.execute(reservations_table_query)
    
    connection.commit()
    
    print("All tables created successfully")
    

except Exception as e:
    print("Error:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
        
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")