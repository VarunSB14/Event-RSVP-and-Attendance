from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .db_utils import *

class RSVP(Resource):
    def get(self, event_id):
        """Get all RSVPs for an event"""
        print(f"[DEBUG] Fetching RSVPs for event ID: {event_id}")
        query = """
            SELECT users.name, rsvps.status
            FROM rsvps
            JOIN users ON users.id = rsvps.user_id
            WHERE rsvps.event_id = %s
        """
        rsvps = exec_get_all(query, (event_id,))
        print(f"[DEBUG] RSVPs fetched: {rsvps}")
        results = [{"name": rsvp[0], "status": rsvp[1]} for rsvp in rsvps]
        return results  
    
    def post(self, event_id):
        """RSVP to an event"""
        data = request.json
        user_id = data.get('user_id')
        print(f"[DEBUG] RSVP attempt: user_id={user_id}, event_id={event_id}")
        
        # Check if event exists and has available spots
        event = exec_get_one("SELECT available_spots FROM events WHERE id = %s", (event_id,))
        if event is None:
            print("[DEBUG] Event not found")
            return {"message": "Event not found"}, 404
        
        available_spots = event[0]
        if available_spots <= 0:
            print("[DEBUG] No available spots")
            return {"message": "No available spots for this event"}
        
        # Check if the user has already RSVP'd
        existing_rsvp = exec_get_one("SELECT id FROM rsvps WHERE user_id = %s AND event_id = %s", (user_id, event_id))
        if existing_rsvp:
            print("[DEBUG] User already RSVP'd")
            return {"message": "User has already RSVP'd to this event"}
        
        # RSVP the user and decrement available spots
        exec_commit("INSERT INTO rsvps (user_id, event_id, status) VALUES (%s, %s, 'RSVP')", (user_id, event_id))
        exec_commit("UPDATE events SET available_spots = available_spots - 1 WHERE id = %s", (event_id,))
        print("[DEBUG] RSVP successful")
        
        return {"message": "RSVP successful"}
    
    def put(self, event_id):
        """Update RSVP status"""
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('status', type=str)
        args = parser.parse_args()
        
        user_id = args['user_id']
        status = args['status']
        
        # Validate status
        if status not in ['RSVP', 'Attended']:
            return {"message": "Invalid status"}
        
        # Check if RSVP exists
        rsvp = exec_get_one("SELECT id FROM rsvps WHERE user_id = %s AND event_id = %s", (user_id, event_id))
        if rsvp is None:
            return {"message": "RSVP not found for this user and event"}
        
        # Update the status
        exec_commit("UPDATE rsvps SET status = %s WHERE user_id = %s AND event_id = %s", (status, user_id, event_id))
        return {"message": "RSVP status updated successfully"}