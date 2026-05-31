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
    
    def __init__(self):
        """Initialize the chatbot service with the configured model provider."""
        self.provider = settings.MODEL_PROVIDER.lower()
        self.temperature = settings.TEMPERATURE
        self.top_p = settings.TOP_P
        self.system_prompt = settings.SYSTEM_PROMPT
        self.max_history = settings.MAX_HISTORY
        
        # Initialize the appropriate provider
        if self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "openai":
            self._init_openai()
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

# Global instance
chatbot_service: Optional[ChatbotService] = None

def get_chatbot_service() -> ChatbotService:
    """Get or create the chatbot service instance."""
    global chatbot_service
    if chatbot_service is None:
        try:
            chatbot_service = ChatbotService()
        except ValueError as e:
            # If API key is not set, create a mock service for development
            print(f"Warning: {str(e)}. Using mock responses.")
            chatbot_service = MockChatbotService()
    return chatbot_service

class MockChatbotService(ChatbotService):
    """Mock chatbot service for development/testing without API keys."""
    
    def __init__(self):
        self.provider = "mock"
        self.system_prompt = settings.SYSTEM_PROMPT
    
    def generate_response(self, user_message: str, conversation_history: List[Message]) -> str:
        """Return mock responses for development."""
        # Simple mock logic
        user_msg_lower = user_message.lower()
        
        mock_responses = {
            "hello": "Hello! How can I help you today?",
            "how are you": "I'm doing great! Thanks for asking. How can I assist you?",
            "what is your name": "I'm an AI Chatbot, your friendly virtual assistant!",
            "what can you do": "I can help answer questions, have conversations, and provide information on various topics.",
            "bye": "Goodbye! Feel free to come back whenever you need help.",
        }
        
        # Check for exact or partial matches
        for key, response in mock_responses.items():
            if key in user_msg_lower:
                return response
        
        # Default response
        return "That's an interesting question! I'm here to help. Could you provide more details?"
