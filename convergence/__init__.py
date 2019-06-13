from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_httpauth

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
http_auth = flask_httpauth.HTTPBasicAuth()
db = SQLAlchemy(app)

from .endpoints import groups_bp, location_bp, auth_bp, core_bp
app.register_blueprint(auth_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(location_bp)
app.register_blueprint(core_bp)