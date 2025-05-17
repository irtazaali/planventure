from app import db
from models import BaseModel
from datetime import datetime, timedelta

class Trip(BaseModel):
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_trips_user'), nullable=False)
    itinerary = db.Column(db.JSON)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('trips', lazy=True))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.itinerary is None and self.start_date and self.end_date:
            self.generate_default_itinerary()
    
    def __repr__(self):
        return f'<Trip {self.title}>'
    
    def generate_default_itinerary(self):
        itinerary = {}
        current_date = self.start_date
        
        while current_date <= self.end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            itinerary[date_str] = {
                'breakfast': {
                    'time': '08:00',
                    'activity': 'Breakfast',
                    'duration': 60,  # minutes
                    'notes': 'Morning meal'
                },
                'lunch': {
                    'time': '13:00',
                    'activity': 'Lunch',
                    'duration': 60,
                    'notes': 'Midday meal'
                },
                'dinner': {
                    'time': '19:00',
                    'activity': 'Dinner',
                    'duration': 90,
                    'notes': 'Evening meal'
                },
                'free_time': {
                    'time': '10:00',
                    'activity': 'Free Time for Activities',
                    'duration': 240,
                    'notes': 'Time for sightseeing, activities, or relaxation'
                }
            }
            current_date += timedelta(days=1)
        
        self.itinerary = itinerary
        db.session.add(self)
        db.session.commit()
        return itinerary
    
    def update_itinerary(self, new_itinerary):
        self.itinerary = new_itinerary
        db.session.add(self)
        db.session.commit()
        return self.itinerary