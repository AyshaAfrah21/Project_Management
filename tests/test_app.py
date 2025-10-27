import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()

def test_login(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'admin'})
    assert response.status_code == 302  # Redirect on success