from database.db_connection import get_db_connection


def add_food_item(business_id, food_name,price,quantity, description, pickup_address, latitude= None, longitude= None, available_until = None):
    
    db = get_db_connection()
    
    # Create a cursor that returns query results as dictionaries
    cursor= db.cursor(dictionary=True)


    try:
        query = """
        INSERT INTO food_listings (
        business_id,
        food_name,
        description,
        price,
        quantity,
        pickup_address,
        latitude,
        longitude,
        available_until
        )

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            business_id,
            food_name,
            description,
            price,
            quantity,
            pickup_address,
            # Latitude and longitude will be populated using
            # the Google Maps Geocoding API based on the pickup address.
            latitude,
            longitude,
            available_until
            )
        
        cursor.execute(query, values)
        db.commit() 
        print("Food listing added successfully.")
        return True, "Food listing added successfully."

    except Exception as e: 
        return False, f"Error adding food listing: {e}" 
    
    finally:
        cursor.close() 
        db.close()
    
## View lisitng:
# 
# def view_food_items(business_id):
#     db = get_db_connection()
#     cursor= db.cursor()

#     try:
#         query = """
#         SELECT * FROM food_listings
#         WHERE business_id = %s
#         ORDER BY  created_at ASC
        
#         """

#         cursor.execute(query, (business_id,))
#         final_list=cursor.fetchall()

#         return final_list
#     except Exception as e:
#         print( "unable to view list due to", e)
#         return None
    
#     finally:
#         cursor.close() 
#         db.close()

# view food listings
def view_food_items(business_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT * FROM food_listings
        WHERE business_id = %s
        ORDER BY created_at ASC
        """
        cursor.execute(query, (business_id,))
        
        # Fetch all food listings belonging to the business. 
        rows = cursor.fetchall()
        # Return the results as a list of dictionaries.
        return rows

    except Exception as e:
        print("Unable to view list due to", e)
        return None

    finally:
        cursor.close()
        db.close()

## Delete from food items:
def delete_item(listing_id, business_id):
    db = get_db_connection()
    cursor= db.cursor()

    try:
        query ="""
        DELETE FROM food_listings
        WHERE listing_id =%s
        AND business_id =%s
        """
        cursor.execute(query, (listing_id, business_id))
        
        # If no rows were affected, the listing was not found
        # or does not belong to this business.
        if cursor.rowcount == 0:
            return False, "Food listings not found."
        db.commit()

        return True, "Food listing deleted successfully"


    except Exception as e :
        return False, f"Error deleteing due to, {e}"
    
    finally:
        cursor.close()
        db.close()

# Update the items in the list 



def update_items(listing_id, business_id, food_name, description, price, quantity, pickup_address, available_until =None,latitude=None, longitude=None):
    db = get_db_connection()
    cursor= db.cursor()

    try:
        query = """
        UPDATE food_listings
        SET
        food_name = %s,
        description = %s,
        available_until = %s,
        price = %s,
        quantity = %s,
        pickup_address = %s,
        latitude = %s,
        longitude = %s
        WHERE listing_id = %s
        AND business_id = %s
        """
        values = (
            food_name,
            description,
            available_until,
            price,
            quantity,
            pickup_address,
            latitude,
            longitude,
            listing_id,
            business_id
        )

        cursor.execute (query, values)
        # If no rows were updated, the listing was not found
        # or no matching business/listing combination exists
        if cursor.rowcount == 0:
            return False, "Food listing not found."
        db.commit()
        return True, "Food listing updated successfully."
    except Exception as e:
        return False, f"Error updating food listing: {e}" 
    finally:
        cursor.close()
        db.close()
        
# Get a single food listing by ID
def get_food_item(listing_id, business_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT *
        FROM food_listings
        WHERE listing_id = %s
        AND business_id = %s
        """

        cursor.execute(query, (listing_id, business_id))

        listing = cursor.fetchone()

        return listing

    except Exception as e:
        print("Unable to retrieve food listing:", e)
        return None

    finally:
        cursor.close()
        db.close()
    
####--