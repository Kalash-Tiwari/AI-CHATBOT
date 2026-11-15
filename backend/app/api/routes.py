"""
API routes for the chatbot application.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.conversation import ChatRequest, ChatResponse, Message
from app.api.chatbot import ChatbotService
from app.config.settings import settings

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
        
        # Get chatbot service for the requested provider or default
        provider = request.provider or settings.MODEL_PROVIDER
        chatbot_service = ChatbotService(provider=provider)
        
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

def _evaluate_provider_status():
    configured_provider = settings.MODEL_PROVIDER.lower().strip()
    gemini_key = bool(settings.GEMINI_API_KEY)
    openai_key = bool(settings.OPENAI_API_KEY)

    active_provider = None
    if configured_provider in {"gemini"} and gemini_key:
        active_provider = "gemini"
    elif configured_provider in {"openai", "gpt", "gpt-4.1", "gpt4"} and openai_key:
        active_provider = "openai"
    elif gemini_key:
        active_provider = "gemini"
    elif openai_key:
        active_provider = "openai"
    else:
        active_provider = "mock"

    missing_keys = []
    if configured_provider == "gemini" and not gemini_key:
        missing_keys.append("GEMINI_API_KEY")
    if configured_provider == "openai" and not openai_key:
        missing_keys.append("OPENAI_API_KEY")
    if configured_provider not in {"gemini", "openai", "gpt", "gpt-4.1", "gpt4"}:
        missing_keys.append("Unsupported MODEL_PROVIDER")

    status = "ready" if active_provider in {"gemini", "openai"} else "mock"
    return {
        "status": status,
        "configured_provider": settings.MODEL_PROVIDER,
        "active_provider": active_provider,
        "gemini_key_set": gemini_key,
        "openai_key_set": openai_key,
        "missing_keys": missing_keys,
        "message": "No real provider key configured; running in mock mode." if active_provider == "mock" else "Provider configuration is valid."
    }

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@router.get("/status")
async def status_check():
    """Status endpoint to verify provider configuration."""
    return _evaluate_provider_status()

@router.post("/clear")
async def clear_chat():
    """Clear the chat history."""
    return {"status": "cleared", "message": "Chat history cleared successfully"}
