from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config=None):
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure SQLAlchemy and other settings
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    if config:
        app.config.update(config)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # CORS Configuration
    cors_config = {
        "origins": [
            "http://localhost:3000",  # React development server
            "http://localhost:5173",  # Vite development server
            os.getenv('FRONTEND_URL', '')  # Production frontend URL
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
    cors.init_app(app, resources={
        r"/api/*": cors_config  # Apply CORS to all /api routes
    })
    
    # Import models AFTER db initialization
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
    
    # Register blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from routes.trips import trips_bp
    app.register_blueprint(trips_bp, url_prefix='/api/trips')
    
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
