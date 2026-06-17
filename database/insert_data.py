from db_connection import get_db_connection

connection = get_db_connection()

try:
    if connection.is_connected():
        print("Connected to the DB successfully.")
        
    cursor = connection.cursor()
    
    # Insert business user
    business_query = """
    INSERT INTO users(
        full_name, email, password_hash,role
    )
    VALUES
    (
        'Fresh Bakery',
        'bakery@email.com',
        'hashed_password',
        'business'    
    )"""
    cursor.execute(business_query)

    #insert customer user
    customer_query = """
    INSERT INTO users
    (full_name, email, password_hash, role)
    VALUES
    ('Faith Muchira',
    'faith@gmail.com',
    'hashed_password',
    'customer'
    )
    """
    
    cursor.execute(customer_query)
    
    # fetch business id 
    cursor.execute("""
            SELECT user_id
            FROM users
            where email = 'bakery@email.com'
            """)
    business_id = cursor.fetchone()[0]
    # fetch customer id
    cursor.execute("""
            SELECT user_id
            FROM users
            WHERE email = 'faith@gmail.com' 
                """)
    customer_id = cursor.fetchone()[0]
    
    # insert food listing
    food_listing_query = """
    INSERT INTO food_listings
    (
        business_id,
        food_name,
        description,
        price,
        quantity,
        pickup_address
    )
    VALUES
    (%s, %s, %s, %s, %s, %s)
    """

    food_listing_values = (
        business_id,
        "Bread Loaf",
        "Fresh bread from today",
        2.50,
        10,
        "12 Main Street, Dublin"
    )

    cursor.execute(
        food_listing_query,
        food_listing_values
    )
    
    # fetch food listing id
    cursor.execute("""
    SELECT listing_id
    FROM food_listings
    WHERE food_name = 'Bread Loaf'
    """)

    listing_id = cursor.fetchone()[0]
    
    # insert food reservation
    reservation_query = """
    INSERT INTO reservations
    (
        customer_id,
        listing_id,
        quantity_reserved,
        status
    )
    VALUES
    (%s, %s, %s, %s)
    """

    reservation_values = (
        customer_id,
        listing_id,
        2,
        "pending"
    )

    cursor.execute(
        reservation_query,
        reservation_values
    )
    
    connection.commit()
    print("Sample data inserted successfully!")

except Exception as e:
    print("Error:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
        
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")