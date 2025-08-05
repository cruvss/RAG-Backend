from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.extractor import extract_text
from app.services.chunking import semantic_chunking, recursive_split_chunking
from app.services.embeddings import generate_embeddings
from app.services.storage_qdrant import upsert_chunks_to_qdrant
from app.services.metadata_store import store_metadata_in_sqlite
from app.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR
from pathlib import Path
import uuid

router = APIRouter()

Path(UPLOAD_DIR).mkdir(exist_ok=True)

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...), chunking: str = "semantic"):
    extension = file.filename.split('.')[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file type")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large")

    text = await extract_text(content, extension)

    if chunking == "semantic":
        chunks = semantic_chunking(text)
    elif chunking == "recursive":
        chunks = recursive_split_chunking(text)
    else:
        raise HTTPException(400, "Invalid chunking strategy")

    embeddings = generate_embeddings(chunks)
    point_ids = [str(uuid.uuid4()) for _ in chunks]

    for idx, pid in enumerate(point_ids):
        store_metadata_in_sqlite(pid, file.filename, idx, len(text.split()), len(text), len(text.split('\n')))

    metadata = [{"source": file.filename, "chunk_index": idx, "id": pid} for idx, pid in enumerate(point_ids)]
    upsert_chunks_to_qdrant(chunks, embeddings, metadata)

    with open(Path(UPLOAD_DIR) / file.filename, "wb") as f:
        f.write(content)

    return {
        "success": True,
        "num_chunks": len(chunks),
        "first_chunk": chunks[0] if chunks else ""
    }
