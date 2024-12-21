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
        
        user = exec_get_one("SELECT id, name FROM users WHERE email = %s AND password = %s", (email, password))
        if user:
            return {"id": user[0], "name": user[1], "message": "Login Successful"}
        return {"message": "invalid credentials"}
    