from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_start_interview():
    # Test valid start request
    payload = {
        "sessionId": "test-session-1",
        "candidate": {
            "member": {"id": "CAND-001"},
            "missions": [{"day": 7, "passed": True}]
        }
    }
    response = client.post("/api/interview", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["done"] is False

def test_continue_interview():
    # Setup session
    client.post("/api/interview", json={
        "sessionId": "test-session-2",
        "candidate": {
            "member": {"id": "CAND-002"},
            "missions": [{"day": 7, "passed": True}]
        }
    })
    
    # Test continue
    payload = {
        "sessionId": "test-session-2",
        "message": "This is a test answer."
    }
    response = client.post("/api/interview", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["done"] is False # because it needs 8 questions minimum
