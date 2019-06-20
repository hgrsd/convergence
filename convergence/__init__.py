"""
convergence-server
A REStful API service that helps you find the ideal place to meet.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_jwt_extended

app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
app.config.from_object('config')
app.config.from_pyfile('config.py')

jwt = flask_jwt_extended.JWTManager(app)

db = SQLAlchemy(app)

from .endpoints import groups_bp, location_bp, user_bp, suggestions_bp
app.register_blueprint(user_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(location_bp)
app.register_blueprint(suggestions_bp)
