from app import db
from models import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone
from flask import current_app

class User(BaseModel):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('username', name='uq_users_username'),
        db.UniqueConstraint('email', name='uq_users_email'),
    )
    
    def set_password(self, password):
        """Set the password hash for the user."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self, token_type='access'):
        """Generate JWT token for the user."""
        expires_delta = (current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] 
                        if token_type == 'access' 
                        else current_app.config['JWT_REFRESH_TOKEN_EXPIRES'])
        
        payload = {
            'user_id': self.id,
            'exp': datetime.now(timezone.utc) + expires_delta,
            'iat': datetime.now(timezone.utc),
            'type': token_type
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def __repr__(self):
        return f'<User {self.email}>'
