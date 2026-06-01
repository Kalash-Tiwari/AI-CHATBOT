"""
Chatbot service for interacting with foundation model APIs.
Supports multiple providers: Gemini, OpenAI, Anthropic, etc.
"""

from typing import List, Optional
from app.config.settings import settings
from app.models.conversation import Message
import google.generativeai as genai
from datetime import datetime

class ChatbotService:
    """Service for handling chatbot responses using foundation models."""
    
    def __init__(self, provider: Optional[str] = None):
        """Initialize the chatbot service with the configured model provider."""
        selected_provider = provider or settings.MODEL_PROVIDER
        self.provider = selected_provider.lower().strip()
        self.temperature = settings.TEMPERATURE
        self.top_p = settings.TOP_P
        self.system_prompt = settings.SYSTEM_PROMPT
        self.max_history = settings.MAX_HISTORY

        # Provider aliases for common naming
        if self.provider in {"gpt", "gpt-4.1", "gpt4", "openai"}:
            self.provider = "openai"
        elif self.provider in {"gemini", "google", "google gemini"}:
            self.provider = "gemini"

        # Initialize the appropriate provider
        if self.provider == "gemini":
            try:
                self._init_gemini()
            except ValueError as gemini_error:
                if settings.OPENAI_API_KEY:
                    self.provider = "openai"
                    self._init_openai()
                else:
                    raise ValueError(
                        "GEMINI_API_KEY not set. Please set GEMINI_API_KEY or switch MODEL_PROVIDER to 'openai' with OPENAI_API_KEY."
                    ) from gemini_error
        elif self.provider == "openai":
            try:
                self._init_openai()
            except ValueError as openai_error:
                if settings.GEMINI_API_KEY:
                    self.provider = "gemini"
                    self._init_gemini()
                else:
                    raise ValueError(
                        "OPENAI_API_KEY not set. Please set OPENAI_API_KEY or switch MODEL_PROVIDER to 'gemini' with GEMINI_API_KEY."
                    ) from openai_error
        else:
            raise ValueError(f"Unsupported model provider: {self.provider}")
    
    def _init_gemini(self):
        """Initialize Google Gemini API."""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in environment variables")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def _init_openai(self):
        """Initialize OpenAI API."""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        # Import here to avoid dependency if not using OpenAI
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_response(self, user_message: str, conversation_history: List[Message]) -> str:
        """
        Generate a response using the foundation model.
        
        Args:
            user_message: The user's current message
            conversation_history: List of previous messages for context
        
        Returns:
            The AI-generated response
        """
        # Limit conversation history to prevent token overflow
        recent_history = conversation_history[-self.max_history:] if conversation_history else []
        
        if self.provider == "gemini":
            return self._generate_gemini_response(user_message, recent_history)
        elif self.provider == "openai":
            return self._generate_openai_response(user_message, recent_history)
    
    def _generate_gemini_response(self, user_message: str, conversation_history: List[Message]) -> str:
        """Generate response using Google Gemini."""
        try:
            # Build the conversation for context
            chat = self.model.start_chat(history=[])
            
            # Add conversation history to the chat
            for msg in conversation_history:
                chat.send_message(
                    msg.content,
                    stream=False
                )
            
            # Get response for the current message
            response = chat.send_message(user_message, stream=False)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating Gemini response: {str(e)}")
    
    def _generate_openai_response(self, user_message: str, conversation_history: List[Message]) -> str:
        """Generate response using OpenAI API."""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history
            for msg in conversation_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating OpenAI response: {str(e)}")

class MockChatbotService(ChatbotService):
    """Mock chatbot service for development/testing without API keys."""
    
    def __init__(self):
        self.provider = "mock"
        self.system_prompt = settings.SYSTEM_PROMPT
        self.temperature = settings.TEMPERATURE
        self.top_p = settings.TOP_P
        self.max_history = settings.MAX_HISTORY
    
    def generate_response(self, user_message: str, conversation_history: List[Message]) -> str:
        """Return mock responses for development."""
        user_msg_lower = user_message.lower()
        
        mock_responses = {
            "hello": "Hello! How can I help you today?",
            "how are you": "I'm doing great! Thanks for asking. How can I assist you?",
            "what is your name": "I'm an AI Chatbot, your friendly virtual assistant!",
            "what can you do": "I can help answer questions, have conversations, and provide information on various topics.",
            "bye": "Goodbye! Feel free to come back whenever you need help.",
        }
        
        for key, response in mock_responses.items():
            if key in user_msg_lower:
                return response
        
        return "I currently do not have an API key configured to fetch real search results. Please add a valid LLM provider key in the backend configuration."
