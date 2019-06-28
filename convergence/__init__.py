"""
convergence-server
A REStful API service that helps you find the ideal place to meet.
"""

import flask_jwt_extended
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=True, static_url_path="/static")
app.config.from_object("config")
app.config.from_pyfile("config.py")

# check if env var is set by seed.py -- if so, follow its db uri
db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
if db_uri:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

db = SQLAlchemy(app)
jwt = flask_jwt_extended.JWTManager(app)

from . import endpoints
from . import error_handling
app.register_blueprint(endpoints.user_bp)
app.register_blueprint(endpoints.events_bp)
app.register_blueprint(endpoints.suggestions_bp)
