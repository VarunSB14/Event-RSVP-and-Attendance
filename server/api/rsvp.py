from flask_restful import Resource
from flask_restful import request
from .db_utils import *

class RSVP(Resource):
    """
    Class to handle RSVP operations for specific events.
    
    Methods:
        get: Retrieve RSVPs for a specific event.
        post: RSVP a user to a specific event.
        put: Update an RSVP status for a specific event.
    """
    
    def get(self, event_id):
        """
        Retrieve all RSVPs for a specific event by its ID.

        Args:
            event_id (int): ID of the event.

        Returns:
            list: List of RSVPs including user details.
        """
        
        query = """
            SELECT users.name, rsvps.status
            FROM rsvps
            JOIN users ON users.id = rsvps.user_id
            WHERE rsvps.event_id = %s
        """
        rsvps = exec_get_all(query, (event_id,))
        results = [{"name": rsvp[0], "status": rsvp[1]} for rsvp in rsvps]
        return results  
    
    def post(self, event_id):
        """
        RSVP a user to a specific event.

        Args:
            event_id (int): ID of the event.

        Returns:
            dict: Success message if RSVP is successful.
        """

        data = request.json
        user_id = data.get('user_id')
        print(f"[DEBUG] RSVP attempt: user_id={user_id}, event_id={event_id}")
        
        # Check if event exists and has available spots
        event = exec_get_one("SELECT available_spots FROM events WHERE id = %s", (event_id,))
        if event is None:
            return {"message": "Event not found"}, 404
        
        available_spots = event[0]
        if available_spots <= 0:
            return {"message": "No available spots for this event"}
        
        # Check if the user has already RSVP'd
        existing_rsvp = exec_get_one("SELECT id FROM rsvps WHERE user_id = %s AND event_id = %s", (user_id, event_id))
        if existing_rsvp:
            return {"message": "User has already RSVP'd to this event"}
        
        # RSVP the user and decrement available spots
        exec_commit("INSERT INTO rsvps (user_id, event_id, status) VALUES (%s, %s, 'RSVP')", (user_id, event_id))
        exec_commit("UPDATE events SET available_spots = available_spots - 1 WHERE id = %s", (event_id,))
        
        return {"message": "RSVP successful"}