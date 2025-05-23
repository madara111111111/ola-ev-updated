from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'viewer'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(300))
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(10))  # 'positive', 'neutral', 'negative'

class Showroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(64), nullable=True)
    map_link = db.Column(db.String(255), nullable=True)
    district = db.Column(db.String(100))
    # For backward compatibility
    location = db.Column(db.String(300))
    google_maps_link = db.Column(db.String(500))

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    top_speed = db.Column(db.String(120), nullable=False)
    battery = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.String(120), nullable=False)
    range = db.Column(db.String(120), nullable=False)
    features = db.Column(db.Text)

# If you have already updated the Vehicle model, you must now migrate your database:
# 1. Delete your old SQLite database file (e.g., instance/app.db) if you don't need the data.
# 2. Recreate the database with the new schema.

# Example (run in Python shell or add to your app startup):
# from codespaces_flask_main.app import db
# db.drop_all()
# db.create_all()
