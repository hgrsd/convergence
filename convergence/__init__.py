"""
convergence-server
A REStful API service that helps you find the ideal place to meet.
"""

import flask_jwt_extended
from flask import Flask

from . import convergence_db


app = Flask(__name__, instance_relative_config=True, static_url_path="/static")
app.config.from_object("config")
app.config.from_pyfile("config.py")
db_url = app.config["DB_URL"]
db = convergence_db.ConvergenceDB(db_url)
jwt = flask_jwt_extended.JWTManager(app)

from . import endpoints
from . import error_handling
app.register_blueprint(endpoints.user_bp)
app.register_blueprint(endpoints.events_bp)
app.register_blueprint(endpoints.suggestions_bp)
app.register_blueprint(endpoints.friends_bp)
