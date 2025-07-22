from flask import Flask
from extension import db
from flask_jwt_extended import JWTManager
from models.task import Task
from models.user import User
from routes.tasks import tasks_bp
from routes.auth import auth_bp
from dotenv import load_dotenv
import os
from config import config_by_name

def create_app():
    load_dotenv()

    # Select config class based on FLASK_ENV
    env = os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[env])

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        if not Task.query.first():
            db.session.add_all([
                Task(task_id=1, task_name='complete project', task_status='completed'),
                Task(task_id=2, task_name='read flask', task_status='pending')
            ])
            db.session.commit()

    @app.route('/')
    def hello():
        return 'Hello world, welcome to Railway!'
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=os.getenv("FLASK_ENV") != "production")

