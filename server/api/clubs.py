from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .swen_344_db_utils import *

class Clubs(Resource):
    def get(self):
        clubs = exec_get_all("SELECT * FROM clubs")
        
        results = []
        for club in clubs:
            results.append({
                "id": club[0],
                "name": club[1],
                "location": club[2],
                "capacity": club[3],
                "yellow_threshold": club[4],
                "current_occupancy": club[5],
                "music": club[6],
            })
        return results

    def post(self):
        data = request.json
        query = """
            INSERT INTO clubs (name, location, capacity, yellow_threshold, current_occupancy, music)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        params = (data['name'], data['location'], data['capacity'], data['yellow_threshold'], data['current_occupancy'], data['music'])
        club_id = exec_insert_returning(query, params)
        return {"id": club_id}
        