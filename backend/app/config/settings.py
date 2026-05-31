import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_TITLE = "AI Chatbot API"
    API_VERSION = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]
    
    # Foundation Model Configuration
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "gemini")  # gemini, openai, claude, etc.
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Model Settings
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P = float(os.getenv("TOP_P", "0.9"))
    
    # System prompt for the chatbot
    SYSTEM_PROMPT = os.getenv(
        "SYSTEM_PROMPT",
        "You are a helpful AI assistant. Answer questions accurately and concisely."
    )

settings = Settings()
