from app import db
from models import BaseModel
from datetime import datetime

class Trip(BaseModel):
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_trips_user'), nullable=False)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('trips', lazy=True))
    
    def __repr__(self):
        return f'<Trip {self.title}>'