from flask import Blueprint, request, jsonify
from app import db
from models.trip import Trip
from schemas.trip_schema import TripSchema
from middleware.auth import token_required
from marshmallow import ValidationError

trips_bp = Blueprint('trips', __name__)
trip_schema = TripSchema()
trips_schema = TripSchema(many=True)

@trips_bp.route('/', methods=['POST'])
@token_required
def create_trip(current_user):
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    try:
        data = trip_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    trip = Trip(
        title=data['title'],
        description=data.get('description'),
        start_date=data['start_date'],
        end_date=data['end_date'],
        location=data.get('location'),
        user_id=current_user.id,
        itinerary=data.get('itinerary')  # Add itinerary field
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify(trip_schema.dump(trip)), 201

@trips_bp.route('/', methods=['GET'])
@token_required
def get_trips(current_user):
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    return jsonify(trips_schema.dump(trips)), 200

@trips_bp.route('/<int:trip_id>', methods=['GET'])
@token_required
def get_trip(current_user, trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify(trip_schema.dump(trip)), 200

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@token_required
def update_trip(current_user, trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    try:
        data = trip_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    trip.title = data['title']
    trip.description = data.get('description')
    trip.start_date = data['start_date']
    trip.end_date = data['end_date']
    trip.location = data.get('location')
    if 'itinerary' in data:  # Update itinerary if provided
        trip.update_itinerary(data['itinerary'])

    db.session.commit()
    return jsonify(trip_schema.dump(trip)), 200

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@token_required
def delete_trip(current_user, trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    db.session.delete(trip)
    db.session.commit()
    return jsonify({"message": "Trip deleted successfully"}), 200
