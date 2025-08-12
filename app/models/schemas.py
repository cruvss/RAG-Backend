from pydantic import BaseModel, EmailStr
from typing import List

class ChatRequest(BaseModel):
    session_id: str
    query: str
    search_method: str = "exact"
    collection: str = "semantic"

class ChatResponse(BaseModel):
    session_id: str
    response: str

class BookingRequest(BaseModel):
    name: str
    email: EmailStr
    date: str  
    time: str
