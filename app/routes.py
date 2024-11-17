from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

def register_routes(app):
    @app.route('/')
    def index():
        return redirect(url_for('home'))

    @app.route('/test_db')
    def test_db():
        try:
            # Get a database connection
            connection = app.get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return f"Database connection successful: {result}"
        except Exception as e:
            return f"Database connection failed: {str(e)}"

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

                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()

                if user and check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    flash('Login successful!')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid email or password!', 'danger')
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
            finally:
                cursor.close()
                connection.close()
        return render_template('login.html')

    @app.route('/home')
    def home():
        return render_template('home.html')
