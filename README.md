[FoodWise Project report - Group 4.pdf](https://github.com/user-attachments/files/29443689/FoodWise.Project.report.-.Group.4.pdf)
# 🥗 FOOD WISE 
## Food Waste Reduction System

## 📌 Overview

The Food Waste Reduction System is a Flask-based web application designed to reduce food waste by connecting businesses with customers who can reserve surplus meals before they are discarded.

The platform supports two types of users:

### 🏪 Business Users

### 👤 Customer Users

---

## 🛠️ Technologies Used

- Python
- Flask
- MySQL
- HTML5
- CSS3
- Google Maps Geocoding API
- Google Maps JavaScript API
- Git & GitHub

---

# ⚙️ Running the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
cd food-waste-reduction-system
```

---

## 2. Create and Activate a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuration

Create a `.env` file in the root directory.

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=food_waste_db

GOOGLE_MAPS_API_KEY=your_google_maps_api_key

SECRET_KEY=your_secret_key
```

## ⚠️ Important

- Replace the database credentials with your own MySQL credentials.
- Add your own Google Maps API key.
- Do **not** commit your `.env` file.
- Sensitive files are excluded using `.gitignore`.

---

# 🗄️ Database Setup

Ensure MySQL is running.

Run the setup script:

```bash
python setup_db.py to create the database 
python create_tables.py to create the tables.
```

This will create:

- `food_waste_db`
- `users`
- `food_listings`
- `reservations`

---

# 🚀 Running the Application

Start the Flask server:

```bash
python server.py
```

Expected output:

```text
Running on http://127.0.0.1:5000/
```

Open your browser and visit:

```
http://127.0.0.1:5000/
```

---

# 👥 User Roles

## 🏪 Business

Business users can:

- Register and log in
- Add surplus food listings
- View their listings
- Update listings
- Delete listings
- Manage available food

---

## 👤 Customer

Customer users can:

- Register and log in
- Browse available meals
- View pickup locations on Google Maps
- Reserve meals
- View their reservations
- Track reservation status

---

# 🗺️ Google Maps Integration

The application uses Google Maps to:

- Convert pickup addresses into latitude and longitude coordinates.
- Display pickup locations on an interactive map.
- Help customers locate businesses offering surplus food.

---

# ✨ Features

- Secure user authentication
- Password hashing
- Session management
- Role-based access control
- CRUD operations for food listings
- Food reservation system
- Reservation status tracking
- Google Maps integration
- Automatic address geocoding
- Input validation
- Responsive user interface

---
# 📂 Project Structure

```text
food-waste-reduction-system/
│
├── backend/
│   ├── __pycache__/
│   ├── food_list.py          # CRUD operations for food listings
│   └── maps.py               # Google Maps geocoding functions
│
├── database/
│   ├── __pycache__/
│   ├── create_tables.py      # Creates database tables
│   ├── db_connection.py      # Database connection helper
│   ├── insert_data.py        # Sample data insertion
│   └── setup_database.py     # Database setup script
│
├── templates/
│   ├── dashboard_business.html   # Business dashboard
│   ├── login.html                # User login page
│   ├── my_reservations.html      # Customer reservations page
│   ├── register.html             # User registration page
│   ├── reservations.html         # Browse available meals
│   └── update_listing.html       # Edit an existing food listing
│
├── Testing/
│   ├── __init__.py
│   ├── test_authentication.py
│   └── test_maps.py
│
├── .env
├── .gitignore
├── app.py
├── authentication.py            # Authentication and password hashing
├── README.md
├── requirements.txt
└── server.py                    # Main Flask application
```

---

# 🔌 Main Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Redirects to login page |
| GET / POST | `/login` | User login |
| GET / POST | `/sign-up` | User registration |
| GET | `/view_items` | Business dashboard |
| GET / POST | `/add_items` | Add a food listing |
| GET / POST | `/update-items/<listing_id>` | Update a food listing |
| GET | `/delete-items/<listing_id>` | Delete a food listing |
| GET | `/reservations` | Browse available meals |
| POST | `/reserve` | Reserve a meal |
| GET | `/my-reservations` | View customer reservations |
| GET | `/logout` | Log out |

---

# 🔒 Security Features

- Password hashing
- Session-based authentication
- Role-based authorization
- Parameterized SQL queries to help prevent SQL injection
- Environment variables for sensitive configuration

---

# 🚀 Future Improvements

Potential future enhancements include:

- Search and filter food listings
- Reservation cancellation
- Business reservation management
- Email notifications
- Food image uploads
- Ratings and reviews
- Mobile responsiveness
- Admin dashboard
- Analytics and reporting

---

# 👩‍💻 Team Members and Log file links

- Faith Daisy Muchira - https://docs.google.com/spreadsheets/d/1xvTETTLb8ECqd-IniqqL-Wda2Usae4rz/edit?usp=sharing&ouid=105359771751620605120&rtpof=true&sd=true
- Lynette Charlene Mbabazi
- Adnya Shinde
- Nirvana Khan
- Aza Aded

---

# 📌 Notes

- Ensure MySQL is running before starting the application.
- Create a valid `.env` file before running the project.
- Install all dependencies from `requirements.txt`.
- Run `setup_db.py` before starting the server.
- Start `server.py` before accessing the application in your browser.
- A Google Maps API key is required for map functionality and automatic address geocoding.
