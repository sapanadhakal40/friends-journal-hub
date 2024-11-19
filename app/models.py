from flask_sqlalchemy import SQLAlchemy
from . import db
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    friends = db.relationship('Friend', backref='user', lazy=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    
    
# class Friend(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     birthday = db.Column(db.Date, nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# class Milestone(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     event = db.Column(db.String(150), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'), nullable=False)