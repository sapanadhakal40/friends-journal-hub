from flask import render_template, request, session, redirect, url_for, flash, current_app,jsonify
from flask_mail import  Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import os
from datetime import datetime, timedelta
from app import mail

from flask_cors import cross_origin
import re 



def register_routes(app):
    @app.route('/')
    def index():
        return redirect(url_for('home'))
    @app.route('/home')
    def home():
        return render_template('home.html')
    
    

    
    
    
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
        cursor = None  # Initialize cursor to None
        connection = None  # Initialize connection to None
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            password_hash = generate_password_hash(password)
            birthdate_str = request.form['birthdate']

            try:
                
                
                if not all ([username,email,password,birthdate_str]):
                    raise ValueError('All fields are required')
                
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', birthdate_str):
                    raise ValueError('Invalid birthdate format.Please use YYYY-MM-DD.')
                birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
                
                password_hash = generate_password_hash(password)
                connection = app.get_db_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, birthdate) VALUES (%s, %s, %s,%s)",
                    (username, email, password_hash, birthdate),
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
                if cursor:
                   cursor.close()
                if connection:
                   connection.close()
        return render_template('register.html')
    
    
    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        cursor = None  # Initialize cursor to None
        connection = None  # Initialize connection to None
        if request.method == 'POST':
            email = request.form.get('email','')
           
            password = request.form['password']
            
            

            try:
                connection = app.get_db_connection()
                cursor = connection.cursor(dictionary=True)
                
                

                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                
                 # Debug: Print the user fetched from the database
                print(f"User fetched: {user}")

        
                if user:
                  print(f"Stored hash: {user['password_hash']}")  # Debug: Print stored hash
                  if check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    session['user_name'] = user['username']
                    session['flash_message'] = 'Login successful!'  # Store flash message in session
                    
                    return redirect(url_for('dashboard'))
                  else:
                    flash('Invalid email or password!', 'danger')
            
                  # Consume remaining results if any
                
                
                
            except Exception as e:
               flash(f'Error: {str(e)}', 'danger')
               print(f"Error: {str(e)}")
            finally:
                if cursor:
                    cursor.fetchall()  
                    cursor.close()
                if connection:
                   connection.close()    
        return render_template('login.html')



  
    
  
    
    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            flash('Please log in to access the dashboard', 'danger')
            return redirect(url_for('login'))
        

        
         
        # Retrieve and flash the message from the session
        if 'flash_message' in session:
            flash(session['flash_message'], 'success')
            session.pop('flash_message', None)  # Remove the message from the session
         
       
        try:
            # Calculate the values for the quick stats
            user_id = session['user_id']
            user_name = session.get('user_name', 'User') 
            connection = app.get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
          
       
            cursor.execute("SELECT id, friend_name, friend_email FROM friends WHERE user_id = %s", (user_id,))
            friends = cursor.fetchall()
            # Calculate completed milestones
        
           
              
            cursor.execute("SELECT COUNT(*) AS completed_count FROM milestones WHERE user_id = %s AND date < NOW()", (user_id,))
            completed_count = cursor.fetchone()['completed_count']
           

  # Calculate upcoming milestones
           
            cursor.execute("SELECT COUNT(*) AS upcoming_count FROM milestones WHERE user_id = %s AND date >= NOW()", (user_id,))
            upcoming_count = cursor.fetchone()['upcoming_count']
           
        
      
        
            # Split milestones into upcoming and completed
            cursor.execute("SELECT * FROM milestones WHERE user_id = %s AND date >= NOW() ORDER BY date ASC", (user_id,))
            upcoming_milestones = cursor.fetchall()

            cursor.execute("SELECT * FROM milestones WHERE user_id = %s AND date < NOW() ORDER BY date DESC", (user_id,))
            completed_milestones = cursor.fetchall()
            
                

            milestones = cursor.fetchall()
         # Calculate days active
            cursor.execute("SELECT MIN(date) AS first_milestone_date FROM milestones WHERE user_id = %s", (user_id,))
            first_milestone_date = cursor.fetchone()['first_milestone_date']
            if first_milestone_date:
                first_milestone_datetime = datetime.combine(first_milestone_date, datetime.min.time())
                days_active = (datetime.now() - first_milestone_datetime).days
            else:
                days_active = 0

        # Retrieve milestones
            cursor.execute("SELECT id, title, description, date, is_completed FROM milestones WHERE user_id = %s", (user_id,))
            milestones = cursor.fetchall()
            
            upcoming_milestones = [m for m in milestones if datetime.combine(m['date'], datetime.min.time()) >= datetime.now()]
            completed_milestones = [m for m in milestones if datetime.combine(m['date'], datetime.min.time()) < datetime.now() ]

        
        finally:
            if cursor:
                cursor.fetchall()  # Ensure all results are read
                cursor.close()
            if connection:
                connection.close()
                    
        return render_template('dashboard.html', user_name=user_name, completed_count=completed_count, upcoming_count=upcoming_count, days_active=days_active, milestones=milestones, upcoming_milestones=upcoming_milestones, completed_milestones=completed_milestones, friends=friends)
    
    
    @app.route('/error')
    def error():
        return render_template('error.html'), 500
    
    @app.route('/add_friend', methods=['GET', 'POST'])
    def add_friend():
        if 'user_id' not in session:
            flash('Please log in to add a friend', 'danger')
            return redirect(url_for('login'))

        if request.method == 'POST':
            user_id = session['user_id']
            friend_name = request.form['friend_name']
            friend_email = request.form['friend_email']

            try:

            # Add friend to the database
                connection = app.get_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO friends (user_id, friend_name, friend_email) VALUES (%s, %s, %s)",
                    (user_id, friend_name, friend_email),
               )
                connection.commit()

                flash('Friend added successfully!', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
            finally:
               if cursor:
                cursor.close()
               if connection:
                connection.close()

        return render_template('add_friend.html')
    
    @app.route('/edit_friend/<int:friend_id>', methods=['GET', 'POST'])
    def edit_friend(friend_id):
        if 'user_id' not in session:
            flash('Please log in to edit a friend', 'danger')
            return redirect(url_for('login'))

        connection = app.get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
        # Fetch the friend's details
           cursor.execute("SELECT * FROM friends WHERE id = %s", (friend_id,))
           friend = cursor.fetchone()

           if not friend or friend['user_id'] != session['user_id']:
              flash('Friend not found or unauthorized access.', 'danger')
              return redirect(url_for('dashboard'))

           if request.method == 'POST':
                friend_name = request.form['friend_name']
                friend_email = request.form['friend_email']

            # Update friend details
                cursor.execute(
                    "UPDATE friends SET friend_name = %s, friend_email = %s WHERE id = %s",
                     (friend_name, friend_email, friend_id)
                )
                connection.commit()

                flash('Friend details updated successfully!', 'success')
                return redirect(url_for('dashboard'))

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return render_template('edit_friend.html', friend=friend)
    
    @app.route('/delete_friend/<int:friend_id>', methods=['POST'])
    def delete_friend(friend_id):
        if 'user_id' not in session:
           flash('Please log in to delete a friend', 'danger')
           return redirect(url_for('login'))

        connection = app.get_db_connection()
        cursor = connection.cursor()
        try:
        # Ensure the friend belongs to the logged-in user
            cursor.execute("SELECT * FROM friends WHERE id = %s AND user_id = %s", (friend_id, session['user_id']))
            friend = cursor.fetchone()
            if not friend:
               flash('Friend not found or unauthorized access.', 'danger')
               return redirect(url_for('dashboard'))

        # Delete the friend
            cursor.execute("DELETE FROM friends WHERE id = %s", (friend_id,))
            connection.commit()
            flash('Friend deleted successfully!', 'success')

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return redirect(url_for('dashboard'))

    
    
    
    @app.route('/add_milestone', methods=['GET', 'POST'])
    def add_milestone():
        if 'user_id' not in session:
            flash('Please log in to add a milestone', 'danger')
            return redirect(url_for('login'))

        if request.method == 'POST':
            user_id = session['user_id']
            title = request.form['title']
            description = request.form['description']
            date = request.form['date']
           

            try:
                connection = app.get_db_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "INSERT INTO milestones (user_id, title, description, date) VALUES (%s, %s, %s, %s)",
                    (user_id, title, description, date),
                )
                connection.commit()

                flash('Milestone added successfully!', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
                print(f"Error: {str(e)}")  # Add this line to print the error to the console
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        return render_template('add_milestone.html')
    
    @app.route('/milestone/<int:id>', methods=['DELETE'])
    @cross_origin()  # Enables CORS for this specific route
    def delete_milestone(id):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401

        try:
            connection = app.get_db_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM milestones WHERE id = %s AND user_id = %s", (id, session['user_id']))
            connection.commit()

            if cursor.rowcount == 0:
                return jsonify({'success': False, 'message': 'Milestone not found'}), 404

            return jsonify({'success': True})
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'success': False, 'message': 'Error deleting milestone'}), 500
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
  
    @app.route('/calendar')
    def calendar():
        if 'user_id' not in session:
            flash('Please log in to access the calendar', 'danger')
            return redirect(url_for('login'))
        return render_template('calendar.html')



    @app.route('/api/events', methods=['GET'])
    @cross_origin()
    def get_events():
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401

        user_id = session['user_id']
        connection = app.get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Fetch milestones
            cursor.execute("""
                SELECT 
                    title, 
                    DATE_FORMAT(date, '%Y-%m-%d') AS start, 
                    'milestone' AS event_type 
                FROM milestones 
                WHERE user_id = %s
            """, (user_id,))
            milestones = cursor.fetchall()

            
        # Fetch user's birthdate
            cursor.execute("SELECT birthdate FROM users WHERE id = %s", (user_id,))
            birthdate_data = cursor.fetchone()
             
            birthdays = []
            if birthdate_data and birthdate_data['birthdate']:
               birthdate = birthdate_data['birthdate']
            if isinstance(birthdate, str):  # Handle birthdate as a string
                birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()

            today = datetime.now().date()
            
            upcoming_birthday = datetime(today.year, birthdate.month, birthdate.day).date()
            if upcoming_birthday < today:
                upcoming_birthday = datetime(today.year + 1, birthdate.month, birthdate.day).date()

            birthdays.append({
                "title": "Birthday",
                "start": upcoming_birthday.strftime("%Y-%m-%d"),
                "event_type": "birthday"
            })

           # Combine milestones and birthdays
            all_events = milestones + birthdays

            return jsonify(all_events)

        except Exception as e:
         # Rollback database changes in case of error
            print(f"Error fetching events: {e}")
            return jsonify({'success': False, 'message': 'Error fetching events'}), 500

        finally:
            cursor.close()
            connection.close()

 
 
 
 
 
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

        # Send email
            msg = Message('Contact Form Submission', sender=email, recipients=['your_email@example.com'])
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            try:
                mail.send(msg)
                flash('Message sent successfully!', 'success')
            except Exception as e:
               flash(f'Error sending message: {str(e)}', 'danger')

            return redirect(url_for('contact'))

        return render_template('contact.html')

    @app.route('/config')
    def config():
     # Display controlled config information
        config_info = {
            'Environment': os.environ.get('FLASK_ENV', 'not set'),
            'Debug': current_app.config.get('DEBUG', 'not set'),
            'Database Host': current_app.config.get('MYSQL_HOST', 'not set')
        }
        return render_template('config.html', config_info=config_info)
    
    @app.route('/logout')
    def logout():
         # Remove username from session
        session.pop('user_id', None)   # Optionally, remove other session keys
        flash("You have been logged out", "info")
        return redirect(url_for('login'))
    
    
   
    
