from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session management

# Connect to MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',  # Replace with your MySQL username
    password='',  # Replace with your MySQL password
    database='strike'  # Replace with your database name
)

cursor = db.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    c_no VARCHAR(15),
    location VARCHAR(100),
    password VARCHAR(255)
)''')
db.commit()

# Route for the landing page
@app.route('/')
def landing_page():
    return render_template('index.html')

# Route for the home page (after login)
@app.route('/home')
def home():
    if 'email' in session:
        cursor.execute("SELECT name, email, c_no, location FROM users WHERE email = %s", (session['email'],))
        user_data = cursor.fetchone()

        if user_data:
            # Convert tuple to dictionary
            user = {
                'name': user_data[0],
                'email': user_data[1],
                'c_no': user_data[2],
                'location': user_data[3]
            }
            return render_template('profile.html', user=user)

    flash("Please log in first.", "error")
    return redirect(url_for('login'))



# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        c_no = request.form['c_no']
        location = request.form['location']
        password = request.form['password']

        # Check if email is already registered
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('register'))

        # Insert user data into MySQL database
        cursor.execute("INSERT INTO users (name, email, c_no, location, password) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, c_no, location, password))
        db.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if not user:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

        # Log the user in
        session['email'] = email
        flash('Login successful!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html')

# Route for logout
'''@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out successfully.', 'success')
    #return redirect(url_for('landing_page'))
    return render_template('index.html')'''

@app.route('/logout')
def logout():
    session.pop('email', None)
    return render_template('logout.html')  # Render a logout confirmation page



if __name__ == '__main__':
    app.run(debug=True)
