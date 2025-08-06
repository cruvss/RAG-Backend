import google.generativeai as genai
from app.services.embeddings import generate_embeddings
from app.services.embeddings import get_qdrant_client
from qdrant_client.models import Filter, SearchParams, PointStruct
from app.models.schemas import BookingRequest
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


def is_booking_intent(user_query: str) -> bool:
    booking_keywords = ["book an interview", "schedule", "appointment", "interview for"]
    return any(keyword in user_query.lower() for keyword in booking_keywords)


import re
import json

def extract_booking_details(text: str) -> dict:
    prompt = f"""
    Extract the following details from the text:
    - Full Name (if not mentioned, leave blank)
    - Email
    - Interview Date
    - Interview Time

    Text: "{text}"

    Respond in strict JSON format like:
    {{
    "name": "Full Name",
    "email": "email@example.com",
    "date": "YYYY-MM-DD",
    "time": "HH:MM"
    }}
    """
    response = model.generate_content(prompt)
    raw = response.text.strip()
    
    # Remove code blocks like ```json ... ```
    cleaned = re.sub(r"```(?:json)?\s*", "", raw).replace("```", "")
    
    

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("⚠️ Gemini responded with invalid JSON:")
        return {}



from app.services.booking_store import save_booking
from app.services.email_service import send_confirmation_email

def handle_booking_flow(user_query: str) -> str:
    booking_data = extract_booking_details(user_query)
    print(type(booking_data))
    
    for k,v in booking_data.items():
        print(type(k)," : ",type(v))
        
    if not all(k in booking_data for k in ("name", "email", "date", "time")):
        return "Sorry, I couldn't understand all the booking details."
    
    name=booking_data["name"]
    email=booking_data["email"]
    date=booking_data["date"]
    time=booking_data["time"]
    
    print(type(name),type(email),type(date),type(time))
    
    booking = BookingRequest(name=name, email=email, date=date, time=time)
    save_booking(booking)
    send_confirmation_email(booking)
    return f"✅ Interview booked for {booking_data['name']} on {booking_data['date']} at {booking_data['time']}."


