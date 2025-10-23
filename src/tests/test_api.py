import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_get_data(client):
    """Test data endpoint"""
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data

def test_create_user(client):
    """Test user creation"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    response = client.post('/api/users', json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] == True
