from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base class for SQLAlchemy models
Base = declarative_base()

class Document(Base):
    """Document model for storing metadata and extracted content."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)  # Primary key for document
    filename = Column(String, unique=True, nullable=False)  # Filename of the uploaded PDF
    upload_date = Column(DateTime, default=datetime.utcnow)  # Upload date of the document
    content = Column(String, nullable=False)  # Extracted content from the PDF
