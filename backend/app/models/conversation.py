from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    """Model for a single message."""
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    """Model for chat request from client."""
    message: str
    conversation_history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    """Model for chat response to client."""
    response: str
    timestamp: Optional[str] = None

class ConversationContext(BaseModel):
    """Model for maintaining conversation context."""
    messages: List[Message] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.messages.append(Message(role=role, content=content))
    
    def get_last_n_messages(self, n: int) -> List[Message]:
        """Get the last n messages."""
        return self.messages[-n:] if len(self.messages) > n else self.messages
    
    def clear(self):
        """Clear conversation history."""
        self.messages = []
