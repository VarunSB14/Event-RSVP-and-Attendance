from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .db_utils import *

class Events(Resource):
    def get(self):
        """Fetch all events"""
        events = exec_get_all("SELECT * FROM events")
        results = []
        for event in events:
            results.append({
                "id": event[0],
                "title": event[1],
                "description": event[2],
                "date": str(event[3]),
                "time": str(event[4]),
                "location": event[5],
                "capacity": event[6],
                "available_spots": event[7]
            })
        return results

    def post(self):
        """Create a new event"""
        data = request.json
        query = """
            INSERT INTO events (title, description, date, time, location, capacity, available_spots)       
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        params = (data['title'], 
                  data['description'], 
                  data['date'], 
                  data['time'], 
                  data['location'], 
                  data['capacity'], 
                  data['capacity']
        )
        event_id = exec_insert_returning(query, params)
        return {"id": event_id}
        