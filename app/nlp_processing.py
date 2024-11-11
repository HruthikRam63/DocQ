def answer_question(question, document_id):
    """Generate an answer based on the question and document."""
    # Retrieve the document from the database using the document_id
    from database import SessionLocal
    from models import Document
    
    db = SessionLocal()
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        return "Document not found!"
    
    # Simple answer generation: This could be extended with NLP models
    # Here, we'll return a simple text search for the question
    # Example: look for the question in the document content
    if question.lower() in document.content.lower():
        return f"Found information on: {question}"
    
    return "Sorry, I couldn't find an answer in the document."
