"""
API routes for the chatbot application.
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.api.chatbot import ChatbotService
from app.config.settings import settings
from app.models.conversation import ChatRequest, ChatResponse, Message

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and return an AI-generated response."""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        provider = request.provider or settings.MODEL_PROVIDER
        chatbot_service = ChatbotService(provider=provider)

        conversation_history = []
        if request.conversation_history:
            for msg in request.conversation_history:
                if isinstance(msg, dict):
                    conversation_history.append(Message(**msg))
                else:
                    conversation_history.append(msg)

        response_payload = chatbot_service.generate_response(
            request.message,
            conversation_history,
            web_search=request.web_search,
            response_mode=request.response_mode,
        )

        if isinstance(response_payload, dict):
            response_text = response_payload.get("text", "")
            sources = response_payload.get("sources", [])
        else:
            response_text = response_payload
            sources = []

        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat(),
            sources=sources,
        )

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(exc)}",
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
        "message": "No real provider key configured; running in mock mode." if active_provider == "mock" else "Provider configuration is valid.",
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
