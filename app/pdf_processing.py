import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    doc = fitz.open(stream=file.file.read(), filetype="pdf")  # Open the PDF file using PyMuPDF
    text = ""
    
    # Loop through each page and extract text
    for page in doc:
        text += page.get_text()  # Extract text from the page
    
    doc.close()  # Close the document
    return text
