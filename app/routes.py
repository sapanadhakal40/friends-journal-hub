from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql

def register_routes(app):
   
    @app.route('/')
    def index():
        return redirect(url_for('home'))
    
    
    
    @app.route('/test_db')
    def test_db():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            result = cur.fetchone()
            cur.close()
            return f"Database connection successful: {result}"
        except Exception as e:
            return f"Database connection failed: {str(e)}"




    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
     if request.method == 'POST':
            # Capture form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)
           
        # if mysql.connection is None:
        #     return "Database connection failed", 500
        cur = mysql.connection.cursor()
        print("Connected to MySQL")
            # Create a cursor to interact with the MySQL database
        try:
         

            # Insert the new user into the 'users' table
           
            cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", 
                            (username, email, password_hash))
            mysql.connection.commit()
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            print(f"Error: {str(e)}") 
            mysql.connection.rollback()
        finally:
            cur.close()
     return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Capture form data
           email = request.form['email']
           password = request.form['password']

            # Create a cursor to interact with MySQL
        try:
                
            cur = mysql.connection.cursor()
            print("Connected to MySQL")
            # Check if the user exists in the database
            cur.execute("SELECT * FROM users WHERE email = %s", [email])
            user = cur.fetchone()

            if user and check_password_hash(user[3], password):  # user[3] is the password_hash
                session['user_id'] = user[0]  # Store the user's ID in the session
                flash('Login successful!')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password!')

        except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
                print(f"Error: {str(e)}")  # Add this line to print the error to the console
        finally:
            cur.close()
        return render_template('login.html')

    @app.route('/home')
    def home():
        return render_template('home.html')