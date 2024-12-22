from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
import hashlib
from .db_utils import *

class Users(Resource):  
    def get(self, user_id=None):
        """Fetch user profile and RSVP'd events"""
        if user_id:
            # Fetch user details
            user = exec_get_one("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
            if not user:
                return {"message": "User not found"}, 404
            
            # Fetch RSVP'd events
            rsvps = exec_get_all("""
                SELECT events.id, events.title, events.date, events.time
                FROM rsvps
                JOIN events ON rsvps.event_id = events.id
                WHERE rsvps.user_id = %s
            """, (user_id,))
            
            return {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "rsvps": [{"id": rsvp[0], "title": rsvp[1], "date": str(rsvp[2]), "time": str(rsvp[3])} for rsvp in rsvps]
            }

        # Fetch all users if no user_id is provided
        users = exec_get_all("SELECT id, name, email FROM users")
        return [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
    
    def post(self):
        """Register a new user"""
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
        print(f"[DEBUG] Password hash for {email}: {hash}")
        
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        exec_commit(query, (name, email, hash))
        return {"message": "User registered successfully"}

    def put(self, user_id):
        """Update user details"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        
        # Check if the user exists
        user = exec_get_one("SELECT id FROM users WHERE id = %s", (user_id,))
        if user is None:
            return {"message": "User not found"}
        
        # Update user details
        query = """
            UPDATE users
            SET name = COALESCE(%s, name), email = COALESCE(%s, email)
            WHERE id = %s
        """
        exec_commit(query, (args.get('name'), args.get('email'), user_id))
        return {"message": "User updated successfully"}
    
    def delete(self, user_id):
        """Delete a user"""
        # Check if the user exists
        user = exec_get_one("SELECT id FROM users WHERE id = %s", (user_id,))
        if user is None:
            return {"message": "User not found"}
        
        # Delete the user
        exec_commit("DELETE FROM users WHERE id = %s", (user_id,))
        return {"message": "User deleted successfully"}
        
            
        
            