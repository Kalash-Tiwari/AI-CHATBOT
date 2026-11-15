# Nexus AI Chatbot

Nexus AI is a full-stack conversational assistant with a modern dashboard, intelligent response handling, and optional web research. It is built with FastAPI for the API and React/Vite for the UI.

## Highlights

- Multi-provider AI support (Gemini and OpenAI)
- Query classification for programming, research, writing, math, and more
- Response-mode control: concise, balanced, and detailed
- Optional web research using public search results
- Follow-up-friendly chat flow and suggested prompts
- Modern glassmorphism-inspired interface
- Graceful fallback to mock mode when no valid API key is configured

## Project structure

```text
AI Chatbot/
├── backend/
│   ├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── __init__.py
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── public/
├── .env.example
├── README.md
├── QUICKSTART.md
└── docker-compose.yml
```

## Quick start

### 1) Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000.

### 2) Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

Open http://localhost:3000 in the browser.

## Configuration

Copy the root `.env.example` file to `.env` and fill in your keys if you want real model responses:

```env
MODEL_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
MODEL_NAME=gemini-1.5-flash
```

If no valid key is configured, the app automatically falls back to mock mode so the chatbot remains runnable.

## API endpoints

- `GET /api/health` — health check
- `GET /api/status` — provider status and configuration summary
- `POST /api/chat` — send a prompt, get a reply, optional web research payload
- `POST /api/clear` — clear the current chat session

## Notes

- The chat request supports `response_mode` values: `concise`, `balanced`, and `detailed`.
- The frontend supports a `Web research` toggle and suggested prompt chips.
- The backend performs lightweight public search scraping for current-information queries when the toggle is enabled.
- Results are shown as source links when available.

## License

MIT
