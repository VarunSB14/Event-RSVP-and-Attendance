import hashlib
from flask_restful import Resource
from flask_restful import request
from .db_utils import *

class Auth(Resource):
    """
    Authentication class for handling user login operations.
    
    Methods:
        post: Validates user credentials and returns login status.
    """
    
    def post(self):
        """
        Handle user login by validating email and hashed password.
        
        Hashes the provided password using SHA-512 and compares it with the stored hash in the database.
        If credentials are valid, returns user details; otherwise, returns an error message.

        Returns:
            dict: A dictionary containing user details and a success message if login is successful.
            tuple: A tuple with an error message and HTTP 401 status code if login fails.
        """
        
        # Parse JSON data from the request
        data = request.json
        email = data.get('email')   # Extract email
        password = data.get('password')   # Extract password
        
        # Hash the input password
        hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
        
        # Query the database to check if the credentials are valid
        query = "SELECT id, name FROM users WHERE email = %s AND password = %s"
        user = exec_get_one(query, (email, hash))
        
        if user:
            # If user exists, return their details
            return {"id": user[0], "name": user[1], "message": "Login Successful"}
        
        # Return an error message if login fails
        return {"message": "invalid credentials"}
    