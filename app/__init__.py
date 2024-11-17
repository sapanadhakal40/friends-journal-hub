from flask import Flask

import mysql.connector

def create_app():
    app = Flask(__name__)

    # MySQL configurations
    app.config['MYSQL_HOST'] = 'localhost'        # MySQL host
    app.config['MYSQL_USER'] = 'root'             # MySQL username
    app.config['MYSQL_PASSWORD'] = ''             # MySQL password
    app.config['MYSQL_DB'] = 'friendjournal'      # MySQL database name
    app.config['MYSQL_PORT'] = 3306               # MySQL port
    app.config['SECRET_KEY'] = b"\xcd'\x10\xc6fu\xab\x84\x9c\x1fx%\xfc\xde\xb05`\x8bPQ\xf1\xb9\xe9}"

    # Function to get a database connection
    def get_db_connection():
        return mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT']
        )

    # Add the connection function to the app for use in routes
    app.get_db_connection = get_db_connection

    # Import and register routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    return app