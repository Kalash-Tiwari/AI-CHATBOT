import os

from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.abspath(os.path.join(base_dir, '..', '..', '.env'))
load_dotenv(dotenv_path)


class Settings:
    """Application settings loaded from environment variables."""

    API_TITLE = "Nexus AI API"
    API_VERSION = "1.1.0"
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]

    # Supported aliases: LLM_PROVIDER and MODEL_PROVIDER
    MODEL_PROVIDER = os.getenv("LLM_PROVIDER") or os.getenv("MODEL_PROVIDER", "gemini")

    # API keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # Model settings
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
    MODEL_NAME = os.getenv("MODEL_NAME") or os.getenv("GEMINI_MODEL") or "gemini-3.8-flash"
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P = float(os.getenv("TOP_P", "0.9"))
    DEFAULT_RESPONSE_MODE = os.getenv("DEFAULT_RESPONSE_MODE", "balanced")

    SYSTEM_PROMPT = os.getenv(
        "SYSTEM_PROMPT",
        "You are Nexus AI, a helpful assistant that can explain complex topics clearly, structure answers with headings, code blocks, and examples, and adapt to the user's context."
    )


settings = Settings()
