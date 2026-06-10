from db_connection import get_server_connection

connection = get_server_connection()

try:
    # Check the connection
    if connection.is_connected():
        print("Connected to the server successfully")
     # create cursor object to execute sql statements
    cursor = connection.cursor()
    
    #create database command
    cursor.execute(
    "CREATE DATABASE IF NOT EXISTS food_waste_db"
    )
    print("Database created successfully!")

except Exception as e:
    print("Error:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")