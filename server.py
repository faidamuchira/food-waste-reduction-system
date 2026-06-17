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
        result = sign_up(name, email, password, role)
        
        if "SUCCESS" in result:
            return redirect(url_for('login'))  # Sends them to the login page
        else:
            return f"Registration Failed: {result}"  # Displays validation error
            
    return render_template('register.html')


# ==========================  LOGIN ROUTE ==================================
@app.route('/log-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Flask uses exact HTML 'name=' attributes to extract the data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # This calls function
        result = log_in(email, password)
        
        if "SUCCESSFUL" in result:
            return f"Welcome! {result}"  # Late user will redirect to the dashboard here
        else:
            return f"Login Failed: {result}"  # Displays "Wrong Password" or "Locked"
            
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)