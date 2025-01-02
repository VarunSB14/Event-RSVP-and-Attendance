from flask_restful import Resource
from flask_restful import reqparse
from .db_utils import *

class Event(Resource):
    """
    Class to handle operations related to a specific event.
    
    Methods:
        get: Retrieve details of a specific event.
        put: Update an existing event.
        delete: Delete an event.
    """
    
    def get(self, event_id):
        """
        Retrieve details of a specific event by its ID.

        Args:
            event_id (int): ID of the event to fetch.

        Returns:
            dict: Details of the event if found.
            tuple: Error message and HTTP 404 status code if event not found.
        """
        
        
        event = exec_get_one("SELECT * FROM events WHERE id = %s", (event_id,))
        if event is None:
            return {"message": "Event not found"}, 404
        
        # Construct the response with event details 
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
        """
        Update details of an existing event.

        Args:
            event_id (int): ID of the event to update.

        Returns:
            dict: Success message upon successful update.
        """
        
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('date', type=str)
        parser.add_argument('time', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('capacity', type=int)
        parser.add_argument('available_spots', type=int)
        args = parser.parse_args()
        
        # Update query and parameters
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
        return {"message": "Event updated successfully"}
        
    def delete(self, event_id):
        """
        Delete an event by its ID.

        Args:
            event_id (int): ID of the event to delete.

        Returns:
            dict: Success message upon successful deletion.
        """
        
        exec_commit("DELETE FROM events WHERE id = %s", (event_id,))
        return {"message": "Event deleted successfully"}
    
    
