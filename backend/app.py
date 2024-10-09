from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'your_password'  # Change to your MySQL password
app.config['MYSQL_DB'] = 'photo_x'

# Initialize MySQL
mysql = MySQL(app)

# Secret key for session management
app.secret_key = 'your_secret_key'  # Change to a strong secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']  # 'store' or 'user'
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (email, password, user_type) VALUES (%s, %s, %s)', (email, password, user_type))
        mysql.connection.commit()
        cursor.close()
        
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        
        if user:
            return redirect(url_for('user_dashboard' if user['user_type'] == 'user' else 'store_dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html')

@app.route('/store_dashboard')
def store_dashboard():
    return render_template('store_dashboard.html')

@app.route('/user_dashboard')
def user_dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM stores')
    stores = cursor.fetchall()
    return render_template('user_dashboard.html', stores=stores)

# Add more routes as needed

if __name__ == '__main__':
    app.run(debug=True)
