from database.db_connection import get_db_connection




def add_food_item(business_id, food_name,price,quantity, description, pickup_address, latitude= None, longitude= None, available_until = None):
    db = get_db_connection()
    cursor= db.cursor()


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


def view_food_items(business_id):
    db = get_db_connection()
    cursor = db.cursor()

    try:
        query = """
        SELECT * FROM food_listings
        WHERE business_id = %s
        ORDER BY created_at ASC
        """
        cursor.execute(query, (business_id,))
        rows = cursor.fetchall()
        
        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]
        # Convert each row to a dictionary
        result = [dict(zip(columns, row)) for row in rows]
        return result

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
        db.commit()

        return True, "item deleted"


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
        db.commit()
        return True, "Food listing updated successfully."
    except Exception as e:
        return False, f"Error updating food listing: {e}" 
    finally:
        cursor.close()
        db.close()
    
####--