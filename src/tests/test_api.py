import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_data():
    """Test data endpoint"""
    response = client.get("/api/v1/data", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_create_user():
    """Test user creation"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    response = client.post(
        "/api/v1/users",
        json=user_data,
        headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True

def test_slow_operation():
    """Test slow operation endpoint"""
    response = client.get("/api/v1/slow-operation", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
