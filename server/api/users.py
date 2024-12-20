from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .db_utils import *

class Users(Resource):
    def get(self, user_id=None):
        """Fetch all users or details of a specific user"""
        if user_id:
            # Fetch a single user by ID
            user = exec_get_one("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
            if user is None:
                return {"message": "User not found"}
            return {"id": user[0], "name": user[1], "email": user[2]}

        # Fetch all users
        users = exec_get_all("SELECT id, name, email FROM users")
        results = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]
        return results
    
    def post(self):
        """Register a new user"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        
        # Check if the email is already registered
        existing_user = exec_get_one("SELECT id FROM users WHERE email = %s", (args['email'],))
        if existing_user:
            return {"message": "Email is already registered"}
        
        # Insert new user
        query = """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        user_id = exec_insert_returning(query, (args['name'], args['email'], args['password']))
        return {"id": user_id, "message": "User registered successfully"}

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
        
            