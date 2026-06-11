import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_server_connection():
    
    """Connect to MySQL server only.
    This is to be used when creating the DB
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")   
    )
    
"""if __name__ == "__main__":
    connection = get_server_connection()
    
    if connection.is_connected():
        print("Connected successfully!")
        
        connection.close()"""

def get_db_connection():
    """Connect to MySQL database, food_waste_db.
    This is to be used when creating the tables, querying, inserting data, and updating records.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")  
    )
    
"""if __name__ == "__main__":
    connection = get_db_connection()
    
    if connection.is_connected():
        print("Connected to database successfully!")
        
    connection.close()"""
    
    
