# Quick Start Guide

## 1) Install dependencies

### Backend
```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## 2) Configure environment

Create a root `.env` file from `.env.example` and add valid keys if you want real model output:

```env
MODEL_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
MODEL_NAME=gemini-1.5-flash
```

If no valid key is present, the app will run in mock mode automatically.

## 3) Run the app

Start the backend:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Start the frontend in another terminal:

```bash
cd frontend
npm run dev -- --host 0.0.0.0 --port 3000
```

Open http://localhost:3000

## 4) Try example prompts

- Explain machine learning in simple terms
- Write Python code to validate API requests
- Compare Python and Java for backend work
- What are the latest AI developments in 2026?
- Summarize database normalization

## Troubleshooting

- If the frontend cannot reach the backend, ensure the API is running on port 8000.
- If the model API key is invalid, the app automatically falls back to mock mode.
- If a port is already in use, change the port or stop the conflicting process.
