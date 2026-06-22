from flask import Flask, render_template, request, redirect, url_for
# This imports exact sign_up and log_in functions
from authentication import sign_up, log_in
from database.db_connection import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    # This runs ONCE to send blank homepage visitors straight to the login route
    return redirect(url_for('login'))

# ========================== REGISTRATION ROUTE ============================
@app.route('/sign-up', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Flask uses exact HTML 'name=' attributes to extract the data
        name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # This calls function
        success, message = sign_up(name, email, password, role)
        
        if success:
            return redirect(url_for('login'))  # Sends them to the login page
        else:
            return f"Registration Failed: {message}"  # Displays validation error
            
    return render_template('register.html')


# ==========================  LOGIN ROUTE ==================================
@app.route('/log-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Flask uses exact HTML 'name=' attributes to extract the data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # This calls function
        success, message, user_data = log_in(email, password)
        
        if success:
           # Send user straight to the map
            return redirect(url_for('dashboard')) 
        else:
            return f"Login Failed: {message}"  # Displays "Wrong Password" or "Locked"
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True) 
    
    try:
        # Get available food that has map coordinates
        cursor.execute("""
            SELECT food_name, description, price, pickup_address, latitude, longitude 
            FROM food_listings 
            WHERE quantity > 0 AND latitude IS NOT NULL AND longitude IS NOT NULL
        """)
        food_items = cursor.fetchall()
        
        # Pass the data to HTML map page
        return render_template('feed.html', listings=food_items)
        
    except Exception as e:
        return f"Database error: {e}"
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)