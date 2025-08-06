from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.services.embeddings import init_qdrant_collection
from app.services.metadata_store import init_sqlite_db
from app.routes.chat import router as chat_router

app = FastAPI(title="RAG Backend Document Processor", version="1.0.1")

@app.on_event("startup")
async def startup_event():
    init_qdrant_collection()
    init_sqlite_db()

app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
