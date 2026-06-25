from flask import Flask, flash, render_template, request, redirect, url_for
# This imports exact sign_up and log_in functions
from authentication import sign_up, log_in
from database.db_connection import get_db_connection

app = Flask(__name__)

def get_user_by_id(user_id):
    """Look a user up by id. Returns the row (dict) or None.
    This REPLACES the old session-based current_user(): instead of reading the
    logged-in user from a session, we receive their id from the page itself."""
    if not user_id:
        return None
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()
        
NOTICES = {
    "ok":           {"type": "success", "text": "Reservation confirmed. See you at pickup!"},
    "low":          {"type": "error",   "text": "Sorry, there was not enough stock left."},
    "gone":         {"type": "error",   "text": "That listing no longer exists."},
    "not_customer": {"type": "error",   "text": "Only customer accounts can reserve meals."},
    "error":        {"type": "error",   "text": "Something went wrong. Please try again."},
}


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
            return redirect(url_for('reservations')) 
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


# ==========================  BROWSE & RESERVE MEALS ROUTE ==================================
@app.route("/reservations")
def reservations():
    """Show available meals AND the map. The logged-in user's id arrives as a
    query parameter"""
    user = get_user_by_id(request.args.get("user_id", type=int))

    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # latitude & longitude are selected too, so the map can plot pins.
        cursor.execute(
            """
            SELECT f.listing_id, f.food_name, f.description, f.price,
                   f.quantity, f.pickup_address, f.available_until,
                   f.latitude, f.longitude,
                   u.full_name AS business_name
            FROM food_listings f
            JOIN users u ON u.user_id = f.business_id
            WHERE f.quantity > 0
              AND (f.available_until IS NULL OR f.available_until > NOW())
            ORDER BY u.full_name, f.food_name
            """
        )
        listings = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    # Optional one-line feedback (?notice=ok etc.) translated to a message.
    notice = NOTICES.get(request.args.get("notice"))
    return render_template("reservations.html", listings=listings, user=user, notice=notice)


@app.route("/reserve", methods=["POST"])
def reserve():
    """Reserve a listing, atomically decrementing its quantity.
    The customer's id comes from a hidden field in the form (set when the page
    was rendered for that logged-in user) -- no session involved."""
    user = get_user_by_id(request.form.get("user_id", type=int))
    if user is None:
        # Not logged in (or id missing) -> back to the login page.
        return redirect(url_for("login"))
    if user["role"] != "customer":
        return redirect(url_for("reservations", user_id=user["user_id"], notice="not_customer"))

    listing_id = request.form.get("listing_id", type=int)
    qty = request.form.get("quantity_reserved", default=1, type=int)
    if not listing_id or qty < 1:
        return redirect(url_for("reservations", user_id=user["user_id"], notice="error"))

    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT food_name, quantity FROM food_listings WHERE listing_id = %s",
            (listing_id,),
        )
        listing = cursor.fetchone()
        if listing is None:
            return redirect(url_for("reservations", user_id=user["user_id"], notice="gone"))

        # Atomic decrement: the WHERE clause guarantees we never oversell, even
        # if two customers reserve the last items at the same moment.
        cursor.execute(
            "UPDATE food_listings SET quantity = quantity - %s "
            "WHERE listing_id = %s AND quantity >= %s",
            (qty, listing_id, qty),
        )
        if cursor.rowcount == 0:
            conn.rollback()
            return redirect(url_for("reservations", user_id=user["user_id"], notice="low"))

        cursor.execute(
            "INSERT INTO reservations "
            "(customer_id, listing_id, quantity_reserved, status) "
            "VALUES (%s, %s, %s, 'pending')",
            (user["user_id"], listing_id, qty),
        )
        conn.commit()
        return redirect(url_for("reservations", user_id=user["user_id"], notice="ok"))

    except mysql.connector.Error:
        conn.rollback()
        return redirect(url_for("reservations", user_id=user["user_id"], notice="error"))
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)

