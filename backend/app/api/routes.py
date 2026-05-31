"""
API routes for the chatbot application.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.conversation import ChatRequest, ChatResponse, Message
from app.api.chatbot import get_chatbot_service

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return an AI-generated response.
    
    Args:
        request: ChatRequest containing the user message and conversation history
    
    Returns:
        ChatResponse with the AI-generated response
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get chatbot service
        chatbot_service = get_chatbot_service()
        
        # Convert message dicts to Message objects if needed
        conversation_history = []
        if request.conversation_history:
            for msg in request.conversation_history:
                if isinstance(msg, dict):
                    conversation_history.append(Message(**msg))
                else:
                    conversation_history.append(msg)
        
        # Generate response
        response_text = chatbot_service.generate_response(
            request.message,
            conversation_history
        )
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@router.post("/clear")
async def clear_chat():
    """Clear the chat history."""
    return {"status": "cleared", "message": "Chat history cleared successfully"}
