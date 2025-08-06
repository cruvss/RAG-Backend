import google.generativeai as genai
from app.services.embeddings import generate_embeddings
from app.services.embeddings import get_qdrant_client
from qdrant_client.models import Filter, SearchParams, PointStruct
from typing import List
from app.config import COLLECTION_NAME
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")



def retrieve_chunks_from_qdrant(query: str, top_k: int = 5) -> List[str]:
    qdrant = get_qdrant_client()

    # Embed the query
    query_vector = generate_embeddings(query)

    # Search Qdrant
    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        search_params=SearchParams(hnsw_ef=128),
    )

    return [hit.payload["text"] for hit in hits if "text" in hit.payload]



def generate_rag_response(query: str, session_id: str) -> str:
    relevant_chunks = retrieve_chunks_from_qdrant(query)
    context = "\n".join(relevant_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    response = model.generate_content(prompt)
    return response.text




