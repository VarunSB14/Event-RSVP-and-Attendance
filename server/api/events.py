from flask_restful import Resource
from flask_restful import reqparse
from .db_utils import *

class Events(Resource):
    """
    Class to handle operations related to multiple events.
    
    Methods:
        get: Retrieve all events.
        post: Create a new event.
    """
    
    def get(self):
        """
        Fetch all events from the database.

        Returns:
            list: List of events with their details.
        """
        
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
        """
        Create a new event.

        Returns:
            dict: ID of the newly created event.
        """
        
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('date', type=str)
        parser.add_argument('time', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('capacity', type=int)
        parser.add_argument('category', type=str)
        args = parser.parse_args()
        
        query = """
            INSERT INTO events (title, description, date, time, location, capacity, available_spots, category)       
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        params = (
                args['title'], 
                args['description'], 
                args['date'], 
                args['time'], 
                args['location'], 
                args['capacity'], 
                args['capacity'],  # Initially, available_spots equals capacity
                args['category']  
        )
        event_id = exec_insert_returning(query, params)
        return {"id": event_id}
        
        