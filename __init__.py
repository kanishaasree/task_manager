from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name
import os

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)
    env = config_name or os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name[env])
    db.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
