from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from utils.auth_utils import get_current_user
from tools.pdf_reader import extract_text_from_pdf

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/extract")
async def extract_pdf(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Sirf PDF file upload karo!")
    
    file_bytes = await file.read()
    
    if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="PDF 10MB se badi nahi honi chahiye!")
    
    text = extract_text_from_pdf(file_bytes)
    
    if not text:
        raise HTTPException(status_code=400, detail="PDF mein koi text nahi mila!")
    
    return {
        "filename": file.filename,
        "text": text,
        "pages": text.count('\n'),
        "chars": len(text)
    }