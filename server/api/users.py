from flask_restful import Resource

from flask_restful import request
import hashlib
from .db_utils import *

class Users(Resource):
    """
    Class to handle operations related to user management.
    
    Methods:
        get: Retrieve user details.
        post: Register a new user.
        put: Update user details.
        delete: Delete a user.
    """
      
    def get(self, user_id=None):
        """
        Retrieve details of a specific user by their ID.

        Args:
            user_id (int): ID of the user.

        Returns:
            dict: User details including RSVP'd events.
        """
        
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
        """
        Register a new user with hashed password.

        Returns:
            dict: Success message upon successful registration.
        """
        
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Hash the password
        hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
        
        # Insert user into the database
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        exec_commit(query, (name, email, hash))
        return {"message": "User registered successfully"}
            
        
            