from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pdf_upload():
    """Test uploading a PDF file."""
    with open("sample.pdf", "rb") as pdf_file:
        response = client.post("/upload_pdf/", files={"file": pdf_file})
    assert response.status_code == 200
    assert "filename" in response.json()
    assert "upload_date" in response.json()

def test_websocket_question_answer():
    """Test WebSocket communication for question answering."""
    with client.websocket_connect("/ws/question_answer/1") as websocket:
        websocket.send_text("What is the document about?")
        response = websocket.receive_text()
        assert response == "Found information on: What is the document about?"

def test_rate_limiting():
    """Test rate limiting."""
    for _ in range(5):
        response = client.get("/upload_pdf/")
        assert response.status_code == 200
    response = client.get("/upload_pdf/")
    assert response.status_code == 429  # Rate limit exceeded
