# Quick Start Guide

## Getting Your API Keys

### Google Gemini
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key to your `.env` file

### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com)
2. Sign in or create an account
3. Go to API keys section
4. Create a new secret key
5. Copy it to your `.env` file

### Anthropic Claude
1. Visit [Anthropic Console](https://console.anthropic.com)
2. Create an account
3. Generate an API key
4. Copy it to your `.env` file

## Running the Application

### Option 1: Local Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn main:app --reload
```

**Frontend (in a new terminal):**
```bash
cd frontend
npm install
npm start
```

### Option 2: Docker Compose

```bash
# Copy and configure environment file
cp .env.example .env
# Edit .env with your API keys

# Build and run containers
docker-compose up --build
```

Access the application at `http://localhost:3000`

## Configuration

Edit `backend/.env`:

```env
# Choose your AI provider
MODEL_PROVIDER=gemini        # Options: gemini, openai, anthropic
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Model settings
MODEL_NAME=gemini-1.5-flash  # Adjust based on your provider
MAX_HISTORY=10               # Number of messages to keep in context
TEMPERATURE=0.7              # Creativity level (0.0-1.0)
TOP_P=0.9                    # Diversity parameter
```

## Features

✅ Real-time AI chat interface
✅ Multi-turn conversation support
✅ Context awareness
✅ Dark mode UI
✅ Support for multiple AI models
✅ RESTful API

## Troubleshooting

### Port Already in Use
- Backend: Change port in `main.py` or use `uvicorn main:app --port 8001`
- Frontend: Set `PORT=3001` environment variable

### CORS Errors
- Ensure backend is running on `http://localhost:8000`
- Check CORS origins in `backend/app/config/settings.py`

### API Key Not Working
- Verify the API key is correct and not expired
- Ensure you're using the right provider
- Check API key permissions

## Project Structure

```
AI Chatbot/
├── frontend/          # React app
├── backend/           # FastAPI server
└── README.md         # Full documentation
```

For detailed documentation, see [README.md](./README.md)
