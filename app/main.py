"""
Main entry point for the RAG Backend Document Processor FastAPI app.
Initializes services and includes API routers.
"""

from fastapi import FastAPI

from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.services.embeddings import init_qdrant_collection
from app.services.metadata_store import init_sqlite_db


app = FastAPI(title="RAG Backend Document Processor", version="1.0.2")

@app.on_event("startup")
async def startup_event() -> None:
    """Initializes qdrant and sqlite on startup"""
    try:
        init_qdrant_collection()
        init_sqlite_db()
    except Exception as e:
        print(f"Startup initialization failed: {e}")

app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
