import os
from datetime import datetime
from flask import (
    Flask, render_template, jsonify, request, abort, redirect,
    send_from_directory)
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from htmlmin.main import minify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, jwt_refresh_token_required, get_jwt_identity,
    get_jti, get_raw_jwt)
from config import BaseConfig
from engineio.async_drivers import gevent  # noqa F401
from models import db

base_config = BaseConfig()


app = Flask(__name__)
app.config.from_object(BaseConfig)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
cors = CORS(app)
