from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.services.embeddings import init_qdrant_collection
from app.services.metadata_store import init_sqlite_db

app = FastAPI(title="RAG Backend Document Processor", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    init_qdrant_collection()
    init_sqlite_db()

app.include_router(upload_router, prefix="/api")
