from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from api.db_utils import *
from api.events import *
from api.event import *
from api.rsvp import *
from api.users import *
from api.authentication import *

app = Flask(__name__) #create Flask instance
CORS(app) #Enable CORS on Flask server to work with Nodejs pages
api = Api(app) #api router

api.add_resource(Events, '/api/events')
api.add_resource(Event, '/api/events/<int:event_id>')
api.add_resource(RSVP, '/api/events/<int:event_id>/rsvp')
api.add_resource(Users, '/api/users', '/api/users/<int:user_id>')
api.add_resource(Auth, '/api/login')

if __name__ == '__main__':
    print("Loading db")
    exec_sql_file('data.sql')
    print("Starting flask")
    app.run(debug=True), #starts Flask