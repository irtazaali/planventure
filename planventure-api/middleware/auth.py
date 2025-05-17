from functools import wraps
from flask import request, jsonify
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                # Extract token from "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid token format"}), 401
        
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        current_user = User.verify_token(token)
        if not current_user:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        if not current_user.is_active:
            return jsonify({"error": "User account is deactivated"}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
