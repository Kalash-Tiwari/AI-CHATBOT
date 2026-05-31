"""
Main FastAPI application for the AI Chatbot.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.routes import router

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI Chatbot API powered by Foundation Models"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI Chatbot API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

# Run with: uvicorn app.main:app --reload
