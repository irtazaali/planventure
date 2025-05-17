# Planventure API 🌍

A Flask-based REST API that powers the Planventure application, helping users create and manage their travel itineraries.

## Features

- 🔐 JWT Authentication
- 📅 Trip Management 
- ✨ Auto-generated Itineraries
- 🗺️ Location Support

## Tech Stack

- Python 3.8+
- Flask
- SQLAlchemy
- JWT Authentication
- SQLite Database
- CORS Support

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git

## Installation

1. Clone the repository and navigate to the API directory:

```sh
git clone https://github.com/yourusername/planventure.git
cd planventure-api
```

2. Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Create environment file:

```sh
cp .sample.env .env
```

5. Update the `.env` file with your configuration:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///planventure.db
CORS_ORIGINS=http://localhost:3000
```

## Database Setup

Initialize the database and run migrations:

```sh
flask db upgrade
python scripts/init_db.py
```

## Running the API

Start the development server:

```sh
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh JWT token

### Trips

- `GET /api/trips` - List all trips
- `POST /api/trips` - Create a new trip
- `GET /api/trips/<id>` - Get trip details
- `PUT /api/trips/<id>` - Update trip
- `DELETE /api/trips/<id>` - Delete trip

## Request Examples

### Register User

```sh
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "traveler",
    "email": "traveler@example.com",
    "password": "SecurePass123"
  }'
```

### Create Trip

```sh
curl -X POST http://localhost:5000/api/trips \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "title": "Paris Adventure",
    "description": "Weekend in Paris",
    "start_date": "2024-06-01T00:00:00",
    "end_date": "2024-06-03T00:00:00",
    "location": "Paris, France"
  }'
```

## Development

### Project Structure

```
planventure-api/
├── app.py              # Application entry point
├── config.py           # Configuration settings
├── requirements.txt    # Project dependencies
├── models/            # Database models
├── routes/            # API routes
├── schemas/           # Data validation schemas
├── middleware/        # Custom middleware
└── migrations/        # Database migrations
```

### Adding New Features

1. Create model in `models/`
2. Add schema in `schemas/`
3. Create routes in `routes/`
4. Register blueprint in `app.py`
5. Run migrations:
   ```sh
   flask db migrate -m "Description"
   flask db upgrade
   ```
