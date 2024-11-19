from flask import Flask
from flask_mail import Mail
from config import DevelopmentConfig, ProductionConfig
import os  
import mysql.connector


mail = Mail()

def create_app():
    app = Flask(__name__)
   
     # Use DevelopmentConfig or ProductionConfig based on environment
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
   
   # Alternatively, directly update mail settings here
    app.config.update({
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': 587,
        'MAIL_USE_TLS': True,
        'MAIL_USE_SSL': False,
        'MAIL_USERNAME': 'Sapanadkl786@gmail.com',
        'MAIL_PASSWORD': 'bnsd rmyg stoz gnuu' , 
        'MAIL_DEFAULT_SENDER': 'Sapanadkl786@gmail.com'  # Default sender
    })

   
     # Debug email settings
    # print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
    # print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
    # print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    # print(f"MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
    # print(f"MAIL_USE_SSL: {app.config['MAIL_USE_SSL']}")
    
    # Initialize Flask-Mail
    mail.init_app(app)


    # Function to get a database connection
    def get_db_connection():
        return mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            # port=app.config['MYSQL_PORT']
        )
       
    # Add the connection function to the app for use in routes
    app.get_db_connection = get_db_connection
    
    
    
   
    # Import and register routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    return app