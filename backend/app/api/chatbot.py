"""
Chatbot service for interacting with foundation model APIs.
"""

import re
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

from app.config.settings import settings
from app.models.conversation import Message


class ChatbotService:
    """Service for handling chatbot responses using foundation models."""

    def __init__(self, provider: Optional[str] = None):
        selected_provider = provider or settings.MODEL_PROVIDER
        self.provider = selected_provider.lower().strip()
        self.temperature = settings.TEMPERATURE
        self.top_p = settings.TOP_P
        self.system_prompt = settings.SYSTEM_PROMPT
        self.max_history = settings.MAX_HISTORY

        if self.provider in {"gpt", "gpt-4.1", "gpt4", "openai"}:
            self.provider = "openai"
        elif self.provider in {"gemini", "google", "google gemini"}:
            self.provider = "gemini"

        gemini_available = bool(settings.GEMINI_API_KEY)
        openai_available = bool(settings.OPENAI_API_KEY)

        if self.provider == "gemini":
            if gemini_available:
                self._init_gemini()
            elif openai_available:
                self.provider = "openai"
                self._init_openai()
            else:
                self._activate_mock()
        elif self.provider == "openai":
            if openai_available:
                self._init_openai()
            elif gemini_available:
                self.provider = "gemini"
                self._init_gemini()
            else:
                self._activate_mock()
        else:
            if gemini_available:
                self.provider = "gemini"
                self._init_gemini()
            elif openai_available:
                self.provider = "openai"
                self._init_openai()
            else:
                self._activate_mock()

    def _init_gemini(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in environment variables")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)

    def _init_openai(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        from openai import OpenAI

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Message],
        web_search: bool = False,
        response_mode: str = "balanced",
    ) -> Dict[str, Any]:
        recent_history = conversation_history[-self.max_history:] if conversation_history else []
        query_category = self._classify_query(user_message)
        search_results = []

        if web_search and self._requires_web_search(user_message, query_category):
            search_results = self._search_web(user_message)

        if self.provider == "gemini":
            return self._generate_gemini_response(
                user_message,
                recent_history,
                query_category,
                search_results,
                response_mode,
            )
        if self.provider == "openai":
            return self._generate_openai_response(
                user_message,
                recent_history,
                query_category,
                search_results,
                response_mode,
            )
        if self.provider == "mock":
            return self._generate_mock_response(
                user_message,
                recent_history,
                query_category,
                search_results,
                response_mode,
            )

        raise Exception(f"No available provider could be initialized for {self.provider}")

    def _activate_mock(self):
        self.provider = "mock"
        self.model = None
        self.client = None

    def _classify_query(self, user_message: str) -> str:
        lower_message = user_message.lower()

        if any(keyword in lower_message for keyword in ["python", "javascript", "java", "code", "debug", "error", "function", "class", "api", "sql", "programming"]):
            return "Programming and Coding"
        if any(keyword in lower_message for keyword in ["math", "equation", "solve", "calculate", "percentage", "algebra", "geometry", "logic", "prove"]):
            return "Mathematics and Logical Reasoning"
        if any(keyword in lower_message for keyword in ["summarize", "notes", "study", "explain", "learn", "concept", "tutorial", "lesson", "education"]):
            return "Education and Learning"
        if any(keyword in lower_message for keyword in ["latest", "current", "now", "today", "news", "2026", "2025", "research", "market", "trend", "recent"]):
            return "Current Information and Web Research"
        if any(keyword in lower_message for keyword in ["compare", "difference", "vs", "pros", "cons", "analysis", "research"]):
            return "Research and Analysis"
        if any(keyword in lower_message for keyword in ["email", "write", "draft", "proposal", "resume", "cover letter", "content", "article"]):
            return "Writing and Content Generation"
        if any(keyword in lower_message for keyword in ["business", "strategy", "marketing", "sales", "team", "management", "report"]):
            return "Business and Professional Tasks"
        if any(keyword in lower_message for keyword in ["translate", "hindi", "spanish", "french", "german", "language"]):
            return "Translation and Language"
        return "General Knowledge"

    def _requires_web_search(self, user_message: str, query_category: str) -> bool:
        lower_message = user_message.lower()
        current_keywords = [
            "latest",
            "current",
            "today",
            "recent",
            "news",
            "2025",
            "2026",
            "upcoming",
            "this week",
            "this month",
            "year",
        ]
        if query_category in {"Current Information and Web Research", "Research and Analysis"}:
            return True
        return any(keyword in lower_message for keyword in current_keywords)

    def _build_strategy_prompt(self, query_category: str, response_mode: str, web_results: List[Dict[str, str]]) -> str:
        mode_map = {
            "concise": "Give a short, direct response with only the most important points.",
            "balanced": "Give a clear, balanced answer with helpful structure and examples.",
            "detailed": "Give a thorough explanation with deeper analysis, examples, and step-by-step breakdowns.",
        }

        base = (
            f"You are Nexus AI, a helpful assistant. "
            f"Query category: {query_category}. "
            f"Response mode: {response_mode}. "
            f"{mode_map.get(response_mode, mode_map['balanced'])} "
            f"Use headings, bullet points, and code blocks when useful. "
            f"If the user asks for code, include a working example and brief explanation. "
            f"If the user asks for comparison, use a table or structured comparison. "
        )

        if web_results:
            source_context = "\n".join(
                f"- {item.get('title', 'Source')}: {item.get('snippet', '')} ({item.get('url', '')})"
                for item in web_results[:5]
            )
            base += f"Use the following current web research context only when relevant: \n{source_context}\n"

        return base

    def _search_web(self, query: str) -> List[Dict[str, str]]:
        encoded_query = quote(query)
        url = f"https://duckduckgo.com/html/?q={encoded_query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results: List[Dict[str, str]] = []

        for result in soup.select(".result")[:5]:
            title_link = result.select_one("a.result-link") or result.select_one("a")
            snippet = result.select_one(".result__snippet") or result.select_one(".snippet")
            if not title_link:
                continue
            title = title_link.get_text(" ", strip=True)
            href = title_link.get("href", "")
            snippet_text = snippet.get_text(" ", strip=True) if snippet else ""
            if title and href:
                results.append({"title": title, "url": href, "snippet": snippet_text})

        return results

    def _build_provider_messages(
        self,
        user_message: str,
        conversation_history: List[Message],
        query_category: str,
        web_results: List[Dict[str, str]],
        response_mode: str,
    ) -> List[Dict[str, str]]:
        system_content = self._build_strategy_prompt(query_category, response_mode, web_results)
        messages = [{"role": "system", "content": system_content}]

        for msg in conversation_history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": user_message})
        return messages

    def _generate_mock_response(
        self,
        user_message: str,
        conversation_history: List[Message],
        query_category: str,
        web_results: List[Dict[str, str]],
        response_mode: str,
    ) -> Dict[str, Any]:
        lower_message = user_message.lower()
        friendly_intro = "Here is a helpful answer based on the current session."

        if "hello" in lower_message:
            response_text = "Hello! I’m Nexus AI. I can explain concepts, write code, summarize notes, and help with research queries."
        elif "how are you" in lower_message:
            response_text = "I’m doing well and ready to help. Ask me to explain a topic, debug code, compare tools, or summarize complex information."
        elif "python" in lower_message and "function" in lower_message:
            response_text = """## Python function example
```python
def greet(name):
    return f'Hello, {name}!'

print(greet('Rahul'))
```
This function takes a name and returns a greeting string.
"""
        elif query_category == "Current Information and Web Research":
            response_text = (
                "## Current information note\n"
                "I can search public sources when web research is enabled, but live verification requires a real API key or a web-search service. "
                "Once connected, I can list recent sources and summarize the most relevant updates."
            )
        else:
            response_text = (
                f"## {query_category}\n"
                f"{friendly_intro}\n\n"
                "- Start with the key idea\n"
                "- Add a concrete example\n"
                "- Include a short takeaway\n\n"
                "Example: if you ask for a summary, I can structure it into key points, examples, and action steps."
            )

        return {"text": response_text, "sources": web_results[:5]}

    def _generate_gemini_response(
        self,
        user_message: str,
        conversation_history: List[Message],
        query_category: str,
        web_results: List[Dict[str, str]],
        response_mode: str,
    ) -> Dict[str, Any]:
        try:
            prompt = self._build_strategy_prompt(query_category, response_mode, web_results)
            prompt += f"\n\nConversation history:\n"
            for msg in conversation_history:
                prompt += f"{msg.role}: {msg.content}\n"
            prompt += f"\nCurrent user message:\n{user_message}\n"

            response = self.model.generate_content(prompt)
            text = getattr(response, "text", str(response)).strip()
            return {"text": text or "I couldn’t generate a response right now.", "sources": web_results[:5]}
        except Exception as exc:
            raise Exception(f"Error generating Gemini response: {str(exc)}") from exc

    def _generate_openai_response(
        self,
        user_message: str,
        conversation_history: List[Message],
        query_category: str,
        web_results: List[Dict[str, str]],
        response_mode: str,
    ) -> Dict[str, Any]:
        try:
            messages = self._build_provider_messages(
                user_message,
                conversation_history,
                query_category,
                web_results,
                response_mode,
            )
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=1200,
            )
            text = response.choices[0].message.content
            return {"text": text, "sources": web_results[:5]}
        except Exception as exc:
            raise Exception(f"Error generating OpenAI response: {str(exc)}") from exc


class MockChatbotService(ChatbotService):
    """Backwards-compatible mock chatbot service."""

    def __init__(self):
        self.provider = "mock"
        self.system_prompt = settings.SYSTEM_PROMPT
        self.temperature = settings.TEMPERATURE
        self.top_p = settings.TOP_P
        self.max_history = settings.MAX_HISTORY

    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Message],
        web_search: bool = False,
        response_mode: str = "balanced",
    ) -> Dict[str, Any]:
        return super()._generate_mock_response(
            user_message,
            conversation_history,
            "General Knowledge",
            [],
            response_mode,
        )
