import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, init_db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_db(app)
        print("Database tables created successfully!")
