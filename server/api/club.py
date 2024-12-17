from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .swen_344_db_utils import *

class Club(Resource):
    def put(self, club_id):
        data = request.json
        query = """
            UPDATE clubs
            SET name = %s, location = %s, capacity = %s, yellow_threshold = %s, current_occupancy = %s, music = %s
            WHERE id = %s
        """
        
        params = (data['name'], data['location'], data['capacity'], data['yellow_threshold'], data['current_occupancy'], data['music'], club_id)
        exec_commit(query, params)
        return {"message": "Club updated successfully"}
        
    def delete(self, club_id):
        exec_commit("DELETE FROM clubs WHERE id = %s", (club_id,))
        return {"message": "Club deleted successfully"}
