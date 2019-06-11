from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_httpauth

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
http_auth = flask_httpauth.HTTPBasicAuth()
db = SQLAlchemy(app)
from .groups import groups
from .auth import auth

app.register_blueprint(auth)
app.register_blueprint(groups)
