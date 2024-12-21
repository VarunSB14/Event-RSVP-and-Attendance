from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .db_utils import *

class Event(Resource):
    def get(self, event_id):
        """Fetch details of a specific event"""
        print(f"Fetching event with ID: {event_id}")
        event = exec_get_one("SELECT * FROM events WHERE id = %s", (event_id,))
        print(f"Event details: {event}")
        if event is None:
            return {"message": "Event not found"}, 404
            
        result = {
            "id": event[0],
            "title": event[1],
            "description": event[2],
            "date": str(event[3]),
            "time": str(event[4]),
            "location": event[5],
            "capacity": event[6],
            "available_spots": event[7]
        }
        return result
    
    def put(self, event_id):
        """Update an existing event"""
        print(f"Updating event with ID: {event_id}")
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('date', type=str)
        parser.add_argument('time', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('capacity', type=int)
        parser.add_argument('available_spots', type=int)
        args = parser.parse_args()
        print(f"Update parameters: {args}")
        
        query = """
            UPDATE events
            SET title = %s, description = %s, date = %s, time = %s, location = %s, capacity = %s, available_spots = %s
            WHERE id = %s
        """
        
        params = (
            args['title'], 
            args['description'], 
            args['date'], 
            args['time'], 
            args['location'], 
            args['capacity'], 
            args['available_spots'], 
            event_id
        )
        exec_commit(query, params)
        print("Event updated successfully")
        return {"message": "Event updated successfully"}
        
    def delete(self, event_id):
        """Delete an event"""
        print(f"Deleting event with ID: {event_id}")
        exec_commit("DELETE FROM events WHERE id = %s", (event_id,))
        print("Event deleted successfully")
        return {"message": "Event deleted successfully"}
    
    
