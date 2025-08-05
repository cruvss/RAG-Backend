import pdfplumber
from io import BytesIO

async def extract_text(file_content: bytes, extension: str) -> str:
    if extension == "pdf":
        with pdfplumber.open(BytesIO(file_content)) as pdf:
            return "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
    elif extension == "txt":
        try:
            return file_content.decode("utf-8")
        except UnicodeDecodeError:
            return file_content.decode("latin-1")
    else:
        raise ValueError("Unsupported file type")
