import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', b"\xcd'\x10\xc6fu\xab\x84\x9c\x1fx%\xfc\xde\xb05`\x8bPQ\xf1\xb9\xe9}")
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'friendjournal')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    
# Email Configuration 
MAIL_SERVER =  os.getenv('MAIL_SERVER','smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
MAIL_USERNAME =  os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    MYSQL_HOST = os.getenv('MYSQL_PROD_HOST', 'prod-db-server')