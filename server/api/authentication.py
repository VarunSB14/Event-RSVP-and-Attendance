import hashlib
from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .db_utils import *

class Auth(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
        print(f"[DEBUG] Hashed password for {email}: {hash}")
        
        query = "SELECT id, name FROM users WHERE email = %s AND password = %s"
        user = exec_get_one(query, (email, hash))
        
        if user:
            print(f"[DEBUG] Login successful for user: {email}")
            return {"id": user[0], "name": user[1], "message": "Login Successful"}
        print(f"[DEBUG] Login failed for user: {email}")
        return {"message": "invalid credentials"}
    