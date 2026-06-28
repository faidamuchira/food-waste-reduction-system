import unittest
import mysql.connector
#import database and function to test them
from authentication import sign_up, log_in, hash_function
from database.db_connection import get_db_connection

class TestAuthentication(unittest. TestCase):
    def setUp(self):
        #Runs before every single test. Clears the database table completely.
        self.connection = get_db_connection()
        self.cursor = self.connection.cursor(dictionary=True)

        #Completely clear out the user test rows so every test starts clean
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.cursor.execute("DELETE FROM reservations")
        self.cursor.execute("DELETE FROM food_listings")
        self.cursor.execute("DELETE FROM users")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        self.connection.commit()

    def tearDown(self):
        #Runs after every single test. Cleans up connection resources.
        self.cursor.close()
        self.connection.close()


    def test_successful_signup_and_login(self):
        #Test a valid user can register and log in.
        #1. Try signing up
        success, message = sign_up("User Name", "user@example.com", "Password123!", "customer")
        self.assertTrue(success)
        self.assertEqual(message, "SUCCESS: Account created successfully")

        #2.verify password was hashed 
        self.cursor.execute("SELECT * FROM users WHERE email = %s", ("user@example.com",))
        db_user = self.cursor.fetchone()

        self.assertIsNotNone(db_user)
        stored_password = db_user["password_hash"]
        self.assertNotEqual(stored_password, "Password123!")
        self.assertEqual(stored_password, hash_function("Password123!"))

        #3. try logging in
        login_success, login_message, user_data = log_in("user@example.com", "Password123!")
        self.assertTrue(login_success)
        self.assertIn("SUCCESSFUL", login_message)
        self.assertIsNotNone(user_data)

    def test_signup_password_validation_length(self):
        #test the password shorter that 8 characters are rejected.
        success, message = sign_up("John Smith", "john@example.com", "Pass1!", "business")
        self.assertFalse(success)
        self.assertEqual(message, "ERROR: Password must be at least 8 characters long")

    def test_signup_password_validation_number(self):
        #test password without at lease one number are rejected
        success, message = sign_up("John Smith", "john@example.com", "Passwordone!", "business")
        self.assertFalse(success)
        self.assertEqual(message, "ERROR: Password must contain at least one number")

    def test_duplicate_email_refistration(self):
        #test taht an email cannot be registered twice.
        sign_up("First User", "duplicate@example.com", "Password123!", "customer")
        success, message = sign_up("Second User", "duplicate@example.com", "NewPass123!", "customer")
        self.assertFalse(success)
        self.assertEqual(message, "ERROR: This Email is already registered!")

    def test_login_invalid_email(self):
        #logging with an email that doesent exist.
        success, message, user_data = log_in("fake@example.com", "Password123!")
        self.assertFalse(success)
        self.assertEqual(message, "ERROR: Email not found!")
        self.assertIsNone(user_data)

    def test_test_account_lockout_after_three_failures(self):
        #Test that an account locks out precisely on the 3rd wrong password attempt.
        # Register a valid user
        sign_up("Bob Ross", "bob@example.com", "BobPass12!", "business")
        
        # 1st Wrong Attempt -> Should show 2 remaining
        success1, message1, _ = log_in("bob@example.com", "WrongPass")
        self.assertFalse(success1)
        self.assertIn("2 attempts remaining", message1)
    
        # 2nd Wrong Attempt -> Should show 1 remaining
        success2, message2, _ = log_in("bob@example.com", "WrongPass")
        self.assertFalse(success2)
        self.assertIn("1 attempts remaining", message2)

        # 3rd Wrong Attempt -> Account locks out
        success3, message3, _ = log_in("bob@example.com", "WrongPass")
        self.assertFalse(success3)
        self.assertEqual(message3, "ERROR: Wrong Password. Account is locked!")

        # 4th Attempt -> Immediate rejection for too many attempts
        success4, message4, _ = log_in("bob@example.com", "BobPass12!") 
        self.assertFalse(success4)
        self.assertEqual(message4, "ERROR: Too many attempts. Account is locked!")

if __name__ == "__main__":
    unittest.main()