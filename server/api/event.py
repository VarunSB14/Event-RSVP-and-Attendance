from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .db_utils import *

class Event(Resource):
    def get(self):
        """Fetch all events or details of a specific event if an event_id is provided"""
        event_id = request.args.get('event_id')
        if event_id:
            event = exec_get_one("SELECT * FROM events WHERE id = %s", (event_id,))
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
        data = request.json
        query = """
            UPDATE events
            SET title = %s, description = %s, date = %s, time = %s, location = %s, capacity = %s, available_spots = %s
            WHERE id = %s
        """
        
        params = (data['title'], 
                  data['description'], 
                  data['date'], 
                  data['time'], 
                  data['location'], 
                  data['capacity'], 
                  data['available_spots'], 
                  event_id
        )
        exec_commit(query, params)
        return {"message": "Event updated successfully"}
        
    def delete(self, event_id):
        exec_commit("DELETE FROM events WHERE id = %s", (event_id,))
        return {"message": "Event deleted successfully"}
    
