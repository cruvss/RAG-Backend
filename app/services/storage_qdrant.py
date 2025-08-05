from qdrant_client.http.models import PointStruct
from app.services.embeddings import qdrant_client
from app.config import COLLECTION_NAME
import uuid

def upsert_chunks_to_qdrant(chunks, embeddings, metadata):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk, **meta}
        )
        for chunk, embedding, meta in zip(chunks, embeddings, metadata)
    ]
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
