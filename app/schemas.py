from pydantic import BaseModel

class DocumentUpload(BaseModel):
    """Schema for uploading documents."""
    filename: str
    content: str
