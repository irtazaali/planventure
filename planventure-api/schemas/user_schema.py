from marshmallow import Schema, fields, validates, ValidationError
import re

class UserRegistrationSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, error_messages={'required': 'Username is required'})
    email = fields.Email(required=True, error_messages={'required': 'Email is required'})
    password = fields.Str(required=True, load_only=True, error_messages={'required': 'Password is required'})
    is_active = fields.Bool(dump_only=True)

    @validates('password')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', value):
            raise ValidationError('Password must contain at least one number')
