from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    goals = db.relationship('Goal', backref='user', lazy=True)

# Goal model with a recommendation field
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    target = db.Column(db.Float, nullable=False)  # Target value (e.g., 10,000 steps)
    current_value = db.Column(db.Float, default=0)  # Current progress (e.g., steps taken)
    progress = db.Column(db.Float, default=0)  # Percentage progress towards goal
    recommendation = db.Column(db.String(500), nullable=True)  # AI-generated recommendation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Progress model
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Float)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
