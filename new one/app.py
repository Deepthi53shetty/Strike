from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session management and flashing messages

# Mock database for demonstration purposes
users_db = {}

# Route for the landing page
@app.route('/')
def landing_page():
    return render_template('h1.html')

# Route for the home page (after login)
@app.route('/home')
def home():
    if 'email' in session:
        user = users_db.get(session['email'])
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        c_no = request.form['c_no']
        location=request.form['location']
        password = request.form['password']

        if email in users_db:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('register'))

        # Save user to the mock database
        users_db[email] = {'name': name, 'email': email,'c_no':c_no,'location':location,'password': password}
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_db.get(email)

        if not user or user['password'] != password:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

        # Log the user in
        session['email'] = email
        flash('Login successful!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    
