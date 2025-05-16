from flask import Blueprint, request, jsonify
from models.user import User
from schemas.user_schema import UserRegistrationSchema
from marshmallow import ValidationError
from app import db
from middleware.auth import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    schema = UserRegistrationSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already taken"}), 400

    user = User(
        username=data['username'],  # Make sure username is included
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    access_token = user.generate_token('access')
    refresh_token = user.generate_token('refresh')

    return jsonify({
        "message": "User registered successfully",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = user.generate_token('access')
    refresh_token = user.generate_token('refresh')

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({
        'message': 'This is a protected route',
        'user': current_user.username
    })
