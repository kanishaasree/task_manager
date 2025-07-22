import pytest
from main import create_app
from extension import db
from models.user import User

@pytest.fixture
def app():
    app = create_app(testing=True)

    with app.app_context():
        db.create_all()

        # ✅ Insert test user
        user = User(username="john")
        user.set_password("12345")  # Use secure password setter
        db.session.add(user)
        db.session.commit()

    yield app  # Provide the app to test


    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
