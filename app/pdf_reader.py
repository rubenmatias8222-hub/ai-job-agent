import io
from pdfminer.high_level import extract_text as pdf_extract
from docx import Document


def extract_text(filename: str, file_bytes: bytes) -> str:
    """
    Extract text from PDF or DOCX uploads
    """

    # PDF FILE
    if filename.lower().endswith(".pdf"):
        try:
            return pdf_extract(io.BytesIO(file_bytes))
        except Exception as e:
            return f"PDF parsing error: {str(e)}"

    # DOCX FILE
    elif filename.lower().endswith(".docx"):
        try:
            doc = Document(io.BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            return f"DOCX parsing error: {str(e)}"

    # FALLBACK
    else:
        return file_bytes.decode("utf-8", errors="ignore")
