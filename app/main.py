from fastapi import FastAPI, UploadFile, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal, init_db
from models import Base, Document
from schemas import DocumentUpload
from pdf_processing import extract_text_from_pdf
from nlp_processing import answer_question
from rate_limiter import rate_limiter

# Initialize FastAPI app
app = FastAPI()

# Initialize the database
init_db()

# Enable CORS if needed (for allowing requests from all domains, you can restrict as required)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile):
    """Endpoint for uploading PDF files."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File type not supported")
    
    # Extract text and save to database
    text = extract_text_from_pdf(file)
    
    # Create a database session
    db = SessionLocal()
    
    # Save the document in the database
    new_doc = Document(filename=file.filename, content=text)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    return {"filename": new_doc.filename, "upload_date": new_doc.upload_date}

@app.websocket("/ws/question_answer/{document_id}")
@rate_limiter  # Applying rate limiting to WebSocket connections
async def question_answer(websocket: WebSocket, document_id: int):
    """WebSocket endpoint for real-time question answering."""
    await websocket.accept()
    
    try:
        while True:
            # Wait for a question from the client
            question = await websocket.receive_text()
            
            # Generate the answer using NLP
            response = answer_question(question, document_id)
            
            # Send the answer back to the client
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print(f"Client {websocket.client} disconnected")

# Start the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
