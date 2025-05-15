from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()
cors = CORS()

def create_app(config=None):
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    
    if config:
        app.config.update(config)
    
    # Initialize extensions with app
    db.init_app(app)
    cors.init_app(app)
    
    # Import models to register them with SQLAlchemy
    from models import User, Trip, BaseModel
    
    # Register routes
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to PlanVenture API"})

    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected" if db.engine.connect() else "disconnected"
        })
    
    return app

def init_db(app):
    with app.app_context():
        # Import models here to ensure they're registered
        from models import User, Trip
        db.create_all()

if __name__ == '__main__':
    app = create_app()
    init_db(app)
    app.run(debug=True)
