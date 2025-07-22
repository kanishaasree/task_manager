from flask import Flask
from extension import db
from flask_jwt_extended import JWTManager  
from models.task import Task
from models.user import User  
from routes.tasks import tasks_bp
from routes.auth import auth_bp  
from dotenv import load_dotenv
import os

def create_app(testing=False):
    load_dotenv()  # ✅ Load from .env file

    app = Flask(__name__)

    # ✅ Read config from environment
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DEV_DATABASE_URI', 'sqlite:///task.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_fallback_key')  # Use env value

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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
