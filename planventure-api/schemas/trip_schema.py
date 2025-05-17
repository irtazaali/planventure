from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class ActivitySchema(Schema):
    time = fields.Str()
    activity = fields.Str()
    duration = fields.Int()
    notes = fields.Str()

class DailyItinerarySchema(Schema):
    breakfast = fields.Nested(ActivitySchema, required=False)
    lunch = fields.Nested(ActivitySchema, required=False)
    dinner = fields.Nested(ActivitySchema, required=False)
    free_time = fields.Nested(ActivitySchema, required=False)

class TripSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    location = fields.Str()
    user_id = fields.Int(dump_only=True)
    itinerary = fields.Dict(
        keys=fields.Str(), 
        values=fields.Nested(DailyItinerarySchema),
        required=False,
        allow_none=True
    )
    
    @validates('end_date')
    def validate_end_date(self, value):
        if 'start_date' in self.context and value < self.context['start_date']:
            raise ValidationError('End date must be after start date')
