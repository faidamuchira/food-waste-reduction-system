from db_connection import get_server_connection

connection = get_server_connection()
cursor = connection.cursor()

cursor.execute(
    "CREATE DATABASE IF NOT EXISTS food_waste_db"
)

print("Database created successfully!")

cursor.close()
connection.close()