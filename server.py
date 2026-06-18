from flask import Flask, render_template, request, redirect, url_for
# This imports exact sign_up and log_in functions
from authentication import sign_up, log_in

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
            user_role = user_data['role']
            user_id = user_data['user_id']
            return f"Welcome! Logged in as user ID {user_id} with the role: {user_role} dashboard."  # Late user will redirect to the dashboard here
        else:
            return f"Login Failed: {message}"  # Displays "Wrong Password" or "Locked"
            
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)