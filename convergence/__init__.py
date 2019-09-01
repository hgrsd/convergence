"""
convergence-server
A REStful API service that helps you find the ideal place to meet.
"""
import logging
import flask_jwt_extended

from flask import Flask
from flask_cors import CORS

from convergence.data import convergence_db


app = Flask(__name__, instance_relative_config=True, static_url_path="/static")
app.config.from_object("config")
app.config.from_pyfile("config.py")
CORS(app, supports_credentials=True)
jwt = flask_jwt_extended.JWTManager(app)

db_url = app.config["DB_URL"]
db = convergence_db.ConvergenceDB(db_url)

logging.basicConfig(filename="logs/Convergence.log", level=logging.INFO)


from convergence.endpoints import user_bp, events_bp, suggestions_bp, \
                                  friends_bp
from convergence.utils import error_handling
app.register_blueprint(user_bp)
app.register_blueprint(events_bp)
app.register_blueprint(suggestions_bp)
app.register_blueprint(friends_bp)
