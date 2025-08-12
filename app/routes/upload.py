from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.extractor import extract_text
from app.services.chunking import semantic_chunking, recursive_split_chunking
from app.services.embeddings import generate_embeddings
from app.services.storage_qdrant import upsert_chunks_to_qdrant
from app.services.metadata_store import store_metadata_in_sqlite
from app.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR
from pathlib import Path
from typing import Optional
import uuid

router = APIRouter()

Path(UPLOAD_DIR).mkdir(exist_ok=True)

@router.post("/upload-document")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    if not file and not text:
        raise HTTPException(400, "You must provide either a file or raw text.")
    if file and text:
        raise HTTPException(400, "Provide only one: file or raw text.")

    if file:
        #  Validate extension
        extension = file.filename.split('.')[-1].lower()
        if extension not in {"pdf", "txt"}:
            raise HTTPException(400, "Only PDF and TXT files are allowed.")
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(413, "File too large")
        text = await extract_text(content, extension)
        filename = file.filename
    else:
        text = text.strip()
        filename = "pasted_text_input.txt"

    # Chunking with both semantic and recursive
    
    chunkings = ['semantic', 'recursive']
    
    chunk_len = dict()
    for chunking in chunkings:
        
        if chunking == "semantic":
            chunks = semantic_chunking(text)
            collection_name = "semantic"
            chunk_sem = len(chunks)
            chunk_len['semantic'] = chunk_sem
            
        elif chunking == "recursive":
            chunks = recursive_split_chunking(text)
            collection_name = "recursive"
            chunk_rec = len(chunks)
            chunk_len['recursive'] = chunk_rec
        else:
            raise HTTPException(400, "Invalid chunking strategy")

        # Embedding + Metadata 
        embeddings = generate_embeddings(chunks)
        point_ids = [str(uuid.uuid4()) for _ in chunks]

        for idx, pid in enumerate(point_ids):
            store_metadata_in_sqlite(pid, filename, idx, len(text.split()), len(text), len(text.split('\n')))

        metadata = [{"source": filename, "chunk_index": idx, "id": pid} for idx, pid in enumerate(point_ids)]
        upsert_chunks_to_qdrant(chunks, embeddings, metadata,collection_name)

    return {
        "success": True,
        "input_type": "file" if file else "text",
        "num_chunks": chunk_len
    }