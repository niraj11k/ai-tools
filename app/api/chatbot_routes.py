"""Chatbot routes."""

from fastapi import APIRouter

from ..core.chatbot_handler import process_chat_message
from ..models.chatbot_models import ChatbotRequest, ChatbotResponse

# Create a new router
router = APIRouter()

@router.post("/chat", response_model=ChatbotResponse)
async def handle_chat_request(chat_request: ChatbotRequest):
    """
    This endpoint receives a user's message, processes it using the handler,
    and returns Lyra's reply.
    """
    # Call the central processing function from the handler
    reply_text = await process_chat_message(chat_request.message)
    
    # Log the user's message and Lyra's reply
    print(f"User: {chat_request.message}")
    print(f"Vani: {reply_text}")    
    
    # Return the response in the format defined by ChatResponse
    return ChatbotResponse(reply=reply_text)
