from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from backend.food_list import add_food_item, view_food_items, update_items, delete_item
# This imports exact sign_up and log_in functions
from authentication import sign_up, log_in
from database.db_connection import get_db_connection
from backend.maps import get_coordinates

app = Flask(__name__)

# secret key so Flask can securely remember user roles
app.secret_key = 'food_wise_secret_session_key'

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
            #Save the user session details
            session['user_id'] = user_data['user_id']
            session['user_name'] = user_data['full_name']

            #direct them based on their roles
            if user_data['role'] == 'business':
                return redirect(url_for('view_items'))
            else:
           # Send user straight to the map if they are customer
                return redirect(url_for('reservations', user_id=user_data['user_id'])) 
        else:
            return f"Login Failed: {message}"  # Displays "Wrong Password" or "Locked"
            
    return render_template('login.html')

@app.route("/logout")
def logout():
    #Remove all session data
    session.clear()
    
    # Return the user to the login page
    return redirect(url_for("login"))

#============================ CUSTOMER  MAP ====================================
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
        return render_template('reservations.html', listings=food_items)
        
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

#============================= BUSINESS ROUTE =================================

@app.route('/view_items')
def view_items():
    # Ensure only logged-in businesses can access this page
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    return render_template("dashbord_business.html") ###

   
@app.route('/api/listings')
def api_listings():
    # Ensure only logged-in businesses can access this page
    if "user_id" not in session:
        return redirect(url_for("login"))
    business_id = session.get('user_id')
        # This is to ensure only authenticated users can  have access 
    if business_id is None:
        return redirect("/login")
    items = view_food_items(business_id)
    return jsonify(items)
    
@app.route('/add_items', methods=['GET', 'POST'])
def add_items():
    
    # Ensure only logged-in businesses can access this page
    if "user_id" not in session:
        return redirect(url_for("login"))

    business_id = session.get("user_id", 1)

    if request.method == "POST":

        food_name = request.form.get("food_name")

        try:
            # Convert form values to the correct data types
            price = float(request.form.get("price"))
            quantity = int(request.form.get("quantity"))

        except (ValueError, TypeError):
            return "Please enter a valid price and quantity."

        # Prevent invalid values from being stored
        if price < 0:
            return "Price cannot be negative."

        if quantity < 1:
            return "Quantity must be at least 1."

        description = request.form.get("description")
        pickup_address = request.form.get("pickup_address")

        # Convert the pickup address into coordinates
        latitude, longitude = get_coordinates(pickup_address)

        if latitude is None or longitude is None:
            return "Unable to locate the pickup address."

        available_until = request.form.get("available_until") or None

        success, message = add_food_item(
            business_id,
            food_name,
            price,
            quantity,
            description,
            pickup_address,
            latitude,
            longitude,
            available_until
        )

        if not success:
            return message

    return redirect("/view_items")
    
@app.route ("/delete-items/<int:listing_id>")
def delete_items_list(listing_id):
    # Ensure only logged-in businesses can access this page
    if "user_id" not in session:
        return redirect(url_for("login"))
    business_id = session.get('user_id', 1)
    success, message = delete_item(
        listing_id,
        business_id
        )
        
    if not success:
        return message
        
    return redirect ("/view_items")

@app.route("/update-items/<int:listing_id>", methods=["GET", "POST"])
def update_items_list(listing_id):
    print("UPDATE CLICKED")
    business_id = session.get('user_id', 1)  # Tracks the real logged-in business
    
    # 1. If the user clicks "Save" inside the edit form, process the changes
    if request.method == "POST":
        print("POST RECEIVED")
        food_name = request.form.get("food_name") 
        price = request.form.get("price") 
        quantity = request.form.get("quantity") 
        description = request.form.get("description") 
        pickup_address = request.form.get("pickup_address")
        
        success, message = update_items(
            listing_id,
            business_id,
            food_name,
            description,
            price,
            quantity,
            pickup_address
        )
        if not success:
            return message
        return redirect("/view_items")

    # 2. If they just click "Update", we need to send them to an edit template
    # We pass the listing_id so the template knows which item is being edited
    return render_template("update_item.html", listing_id=listing_id)

if __name__ == '__main__':
    app.run(debug=True)