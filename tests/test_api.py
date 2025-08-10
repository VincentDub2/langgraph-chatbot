"""
Tests pour l'API FastAPI
"""
import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)


def test_root_endpoint():
    """Test du point d'entrée racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Chatbot Agent Immobilier API"
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    """Test du point d'entrée de santé"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


def test_chat_endpoint():
    """Test du point d'entrée de chat"""
    response = client.post("/chat/", json={
        "message": "Bonjour",
        "stream": False
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "thread_id" in data
    assert "timestamp" in data


def test_agents_endpoint():
    """Test du point d'entrée des agents"""
    response = client.get("/agents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_properties_endpoint():
    """Test du point d'entrée des propriétés"""
    response = client.get("/properties/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
