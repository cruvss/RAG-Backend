from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from app.config import COLLECTION_NAME

import os

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)


def generate_embeddings(chunks):
    return model.encode(chunks, show_progress_bar=False).tolist()

def init_qdrant_collection(vector_size: int = 384):
    collections = qdrant_client.get_collections().collections
    for collect in COLLECTION_NAME:
        if collect not in [c.name for c in collections]:
            qdrant_client.recreate_collection(
                collection_name=collect,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
