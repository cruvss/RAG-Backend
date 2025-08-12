from qdrant_client.http.models import PointStruct
from app.services.embeddings import qdrant_client
import uuid

def upsert_chunks_to_qdrant(chunks, embeddings, metadata, collection_name):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk, **meta}
        )
        for chunk, embedding, meta in zip(chunks, embeddings, metadata)
    ]
    qdrant_client.upsert(collection_name=collection_name, points=points)
