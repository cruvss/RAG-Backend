from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, BookingRequest
from app.services.rag_engine import generate_rag_response
from app.services.redis_memory import store_message, fetch_history
from app.services.booking_store import save_booking
from app.services.email_service import send_confirmation_email

router = APIRouter()

# @router.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     try:
#         history = fetch_history(request.session_id)
#         response_text = generate_rag_response(request.query, history)
#         store_message(request.session_id, request.query, response_text)
#         return ChatResponse(session_id=request.session_id, response=response_text)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

import traceback

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        history = fetch_history(request.session_id)
        response_text = generate_rag_response(request.query, history)
        store_message(request.session_id, request.query, response_text)
        return ChatResponse(session_id=request.session_id, response=response_text)
    except Exception as e:
        print("❌ Error in /chat:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/book-interview")
async def book_interview(booking: BookingRequest):
    try:
        save_booking(booking)
        send_confirmation_email(booking)
        return {"message": "Interview booked and confirmation sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")
