import PyPDF2
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """PDF se text extract karo"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"PDF read error: {str(e)}"