from db_connection import get_db_connection

connection = get_db_connection()

try:
    if connection.is_connected():
        print("Connected to the DB successfully.")
        
    cursor = connection.cursor(buffered=True)
    
    # Insert business user
    business_query = """
    INSERT INTO users(
        full_name, email, password_hash, role, attempts
    )
    VALUES
    (
        'Fresh Bakery',
        'bakery@email.com',
        'hashed_password',
        'business',
        0    
    )"""
    cursor.execute(business_query)

    #insert customer user
    customer_query = """
    INSERT INTO users
    (full_name, email, password_hash, role, attempts)
    VALUES
    ('Faith Muchira',
    'faith@gmail.com',
    'hashed_password',
    'customer',
    0
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
    
    # insert multiple food listings
    food_listing_query = """
    INSERT INTO food_listings
    (
        business_id,
        food_name,
        description,
        price,
        quantity,
        pickup_address,
        latitude,
        longitude
    )
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    food_listing_values = [
        # Dublin 
        (business_id, "Bread Loaf", "Fresh bread from today", 2.50, 10, "12 Main Street, Dublin", 53.349805, -6.260310),
        # London
        (business_id, "Surplus Pastry Box", "Croissants and muffins.", 3.50, 5, "15 Baker St, London", 51.5236, -0.1585),
        # Manchester
        (business_id, "Organic Veggie Bundle", "Carrots, potatoes, and onions.", 2.00, 10, "42 Northern Quarter, Manchester", 53.4830, -2.2355),
        # Edinburgh
        (business_id, "End of Day Sandwiches", "Meat and vegetarian sandwiches.", 1.50, 8, "8 Royal Mile, Edinburgh", 55.9500, -3.1900),
        # Cardiff
        (business_id, "Bagel Batch", "Plain and sesame bagels.", 2.50, 3, "12 Castle Arcade, Cardiff", 51.4800, -3.1790),
        # Belfast
        (business_id, "Mixed Dairy Box", "Milk, butter, and yogurt.", 4.00, 4, "9 Titanic Quarter, Belfast", 54.6040, -5.9080)
    ]

    cursor.executemany(
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