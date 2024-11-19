from flask import render_template, request, session, redirect, url_for, flash, current_app
from flask_mail import  Message
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import os
from app import mail



def register_routes(app):
    @app.route('/')
    def index():
        return redirect(url_for('home'))
    
    
    @app.route('/test_email')
   
          
    def test_email():
        try:
            msg = Message(
                subject='Test Email',
                sender='Sapanadkl786@gmail.com',  # Specify the sender
                recipients=['your_email@gmail.com'],  # Replace with your test email
                body='This is a test email from Flask.'
            )
            mail.send(msg)
            return "Flask-Mail: Email sent successfully!"
        except Exception as e:
           return f"Failed to send email: {str(e)}"
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            password_hash = generate_password_hash(password)

            try:
                connection = app.get_db_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, password_hash),
                )
                connection.commit()
                
                 # Send confirmation email
                msg = Message(
                    subject='Welcome to My App',
                    recipients=[email],
                    body='Thank you for registering!'
                 )
                mail.send(msg)

                
                flash('You are now registered and can log in', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
            finally:
                cursor.close()
                connection.close()
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            try:
                connection = app.get_db_connection()
                cursor = connection.cursor(dictionary=True)
                
                  # Debug: Print the email entered
                print(f"Email entered: {email}")

                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                
                 # Debug: Print the user fetched from the database
                print(f"User fetched: {user}")

                if user and check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    flash('Login successful!')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid email or password!', 'danger')
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
                print(f"Error: {str(e)}")
            finally:
                cursor.close()
                connection.close()
        return render_template('login.html')
  



    @app.route('/home')
    def home():
        return render_template('home.html')
    
    
    @app.route('/config')
    def config():
     # Display controlled config information
        config_info = {
            'Environment': os.environ.get('FLASK_ENV', 'not set'),
            'Debug': current_app.config.get('DEBUG', 'not set'),
            'Database Host': current_app.config.get('MYSQL_HOST', 'not set')
        }
        return render_template('config.html', config_info=config_info)
    
    
    # @app.route('/logout')
    # def logout():
    #  session.clear()
    # flash("You have been logged out", "info")
    # return redirect(url_for('login'))
    # @app.route('/test_db')
    # def test_db():
    #     try:
    #         # Get a database connection
    #         connection = app.get_db_connection()
    #         cursor = connection.cursor()
    #         cursor.execute("SELECT 1")
    #         result = cursor.fetchone()
    #         cursor.close()
    #         connection.close()
    #         return f"Database connection successful: {result}"
    #     except Exception as e:
    #         return f"Database connection failed: {str(e)}"
