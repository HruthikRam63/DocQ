

* * *

DocQ: PDF-Based Question Answering Backend
==========================================

**DocQ** is a backend service that allows users to upload PDF documents and ask questions about their content in real-time. It uses FastAPI for backend APIs, WebSocket for real-time question-answering, and integrates NLP processing to answer questions based on the PDF content.

Features
--------

*   **PDF Upload**: Allows users to upload PDF documents and store the extracted content for analysis.
*   **Real-Time Question Answering**: Users can connect via WebSocket to ask questions about the PDF content and receive real-time answers.
*   **Session-Based Context**: Supports follow-up questions in the same WebSocket session.
*   **Rate Limiting**: Controls API usage to manage server load and prevent abuse.
*   **SQLite Database**: Stores document metadata and extracted content.

* * *

Prerequisites
-------------

*   **Python** 3.8 or higher
*   Recommended tools: [Postman](https://www.postman.com/) (for testing HTTP and WebSocket endpoints), [wscat](https://github.com/websockets/wscat) (for WebSocket testing)

Project Structure
-----------------

```plain text
DocQ/
├── main.py              # Main FastAPI application with endpoints
├── database.py          # Database setup and initialization
├── models.py            # Database models (Document model)
├── schemas.py           # Pydantic schemas for input/output validation
├── pdf_processing.py    # PDF text extraction using PyMuPDF
├── nlp_processing.py    # NLP processing for question-answering
├── rate_limiter.py      # In-memory rate limiter for API and WebSocket
├── tests/               # Directory for test scripts
│   ├── test_endpoints.py    # Tests for API endpoints and WebSocket
│   └── test_rate_limiting.py # Tests for rate limiting functionality
└── requirements.txt     # List of dependencies
```

* * *

Setup Instructions
------------------

1.  **Clone the Repository**
    
    ```bash
    git clone <repo_url> cd DocQ
    ```
2.  **Install Dependencies**
    
    Install the project dependencies using `requirements.txt`.
    
    ```bash
    pip install -r requirements.txt
    ```
3.  **Initialize the Database**
    
    Run the following command to set up the SQLite database:
    
    ```bash
    python database.py
    ```
    
    This will create a `docq.db` SQLite database file with the required tables.
    
4.  **Start the FastAPI Application**
    
    Use `uvicorn` to run the FastAPI application.
    
    ```bash
    uvicorn main:app --reload
    ```
    By default, the app will run on `http://127.0.0.1:8000`.
    

* * *

API Endpoints
-------------

### 1\. **PDF Upload Endpoint**

*   **URL**: `/upload_pdf/`
*   **Method**: `POST`
*   **Description**: Upload a PDF document to be stored and processed.
*   **Request**:
    *   `file`: The PDF file to be uploaded.
*   **Response**: Returns the filename and upload date if successful.

**Example Request (using `curl`)**:

```bash
curl -X POST "http://127.0.0.1:8000/upload_pdf/" -F "file=@path/to/sample.pdf"
```

### 2\. **WebSocket Question Answering Endpoint**

*   **URL**: `/ws/question_answer/{document_id}`
*   **Method**: `WebSocket`
*   **Description**: Connect via WebSocket to ask questions about the PDF content in real-time.
*   **Parameters**:
    *   `document_id`: The ID of the uploaded document.
*   **Usage**:
    *   Connect to the WebSocket endpoint and send a question as a message.
    *   The server responds with answers based on the uploaded document’s content.

**Example Usage (using `wscat`)**:

```bash

wscat -c ws://127.0.0.1:8000/ws/question_answer/1
```
After connecting, send questions, e.g., `"What is the document about?"`

* * *

Testing
-------

The project includes tests to verify the functionality of the endpoints, WebSocket question answering, and rate limiting.

### Running Tests

1.  **Navigate to the Project Directory**
    
    ```bash
       cd DocQ
    ```
2.  **Run Tests Using Pytest**
    
    ```bash
    pytest tests/
    ```
    This will execute all tests in the `tests` directory, including:
    
    *   **PDF Upload Test**: Verifies the `/upload_pdf/` endpoint.
    *   **WebSocket Test**: Tests real-time question-answering functionality.
    *   **Rate Limiting Test**: Ensures rate limiting is properly enforced.

### Example Test Cases

*   **PDF Upload**: Checks if the server correctly stores PDF content and metadata.
*   **WebSocket Question Answering**: Tests if the WebSocket can handle questions and maintain context within a session.
*   **Rate Limiting**: Simulates multiple requests to test if rate limiting is applied correctly.

* * *

Additional Information
----------------------

*   **File Storage**: Uploaded PDFs are stored in the database along with their extracted text.
*   **NLP Integration**: The question-answering function is a placeholder; it can be extended with more complex NLP models for advanced question answering.
*   **Rate Limiting**: Configured to allow 5 requests per minute per client.

* * *
