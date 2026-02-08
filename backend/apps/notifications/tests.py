from ninja.testing import TestClient
from apps.notifications.views import router

# Create your tests here.
client = TestClient(router)

def test_create_email_notification():
    response = client.post('/', json={
        "user": 1,
        "ticket": 1,
        "event": "CREATED",
        "status": "SENT"
    })
    
    assert response.status_code == 200
    
