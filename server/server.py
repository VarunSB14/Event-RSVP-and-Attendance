from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from api.db_utils import *
from api.events import *
from api.event import *

app = Flask(__name__) #create Flask instance
CORS(app) #Enable CORS on Flask server to work with Nodejs pages
api = Api(app) #api router

api.add_resource(Events, '/api/events')
api.add_resource(Event, '/api/events/<int:event_id>')

if __name__ == '__main__':
    print("Loading db")
    exec_sql_file('data.sql')
    print("Starting flask")
    app.run(debug=True), #starts Flask