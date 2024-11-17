from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    
    # MySQL configurations
    app.config['MYSQL_HOST'] = 'localhost'  # host of MySQL server
    app.config['MYSQL_USER'] = 'root'  # MySQL username
    app.config['MYSQL_PASSWORD'] = ''  #  MySQL password
    app.config['MYSQL_DB'] = 'friendjournal'  # The database created in phpMyAdmin
    app.config['SECRET_KEY']= b"\xcd'\x10\xc6fu\xab\x84\x9c\x1fx%\xfc\xde\xb05`\x8bPQ\xf1\xb9\xe9}"
    
    app.config['MYSQL_PORT'] = 3306 
 # Initialize MySQL
    mysql.init_app(app)
   
   
    with app.app_context():
     from .routes import register_routes
     register_routes(app)



    return app