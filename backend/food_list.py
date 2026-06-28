
from database.db_connection import get_db_connection

class FoodItems:
    def __init__(self, business_id):
        self.business_id= business_id
    def add_food_item(self, food_name,price,quantity, description, pickup_address, latitude= None, longitude= None, available_until = None):
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
            self.business_id,
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
            print("Food Item  added successfully.")
            return True, "Food item has been added successfully."

        except Exception as e: 
            return False, f"Error adding food item: {e}" 
        
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


    def view_food_items(self):
        db = get_db_connection()
        cursor = db.cursor()

        try:
            query = """
            SELECT * FROM food_listings
            WHERE business_id = %s
            ORDER BY created_at ASC
            """
            cursor.execute(query, (self.business_id,))
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
    def delete_item(self, listing_id):
        db = get_db_connection()
        cursor= db.cursor()

        try:
            cursor.execute(
                "DELETE FROM reservations WHERE listing_id=%s",
                (listing_id,))
            #query ="""
            #DELETE FROM food_listings
            #WHERE listing_id =%s
            #AND business_id =%s
            #"""
            cursor.execute("DELETE FROM food_listings WHERE listing_id=%s AND business_id=%s",
                           (listing_id, self.business_id))
            
            if cursor.rowcount == 0:
                return False, "Listing not found."
        
            #cursor.execute(query, (listing_id, self.business_id))
            db.commit()

            return True, "item deleted"


        except Exception as e :
            return False, f"Error deleteing due to, {e}"
        
        finally:
            cursor.close()
            db.close()

    
    # Update the items in the list 

    def update_items(self, listing_id, food_name, description, price, quantity, pickup_address, available_until =None,latitude=None, longitude=None):
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
                self.business_id
            )

            cursor.execute (query, values)
            db.commit()
            return True, "Food listing updated successfully."
        except Exception as e:
            return False, f"Error updating food listing: {e}" 
        finally:
            cursor.close()
            db.close()
        
    def get_food_item(self, listing_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            query = """
            SELECT *
            FROM food_listings
            WHERE listing_id = %s
            AND business_id = %s
            """

            cursor.execute(query, (listing_id, self.business_id))

            listing = cursor.fetchone()

            return listing

        except Exception as e:
            print("Unable to retrieve food listing:", e)
            return None

        finally:
            cursor.close()
            db.close()
    
    ####--