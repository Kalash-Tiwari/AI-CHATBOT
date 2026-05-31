# AI Chatbot Project

A full-stack AI chatbot application with React frontend and FastAPI backend, powered by foundation model APIs.

## Features

- **Real-time Chat Interface**: Interactive chat UI built with React and Tailwind CSS
- **Multi-turn Conversations**: Maintains conversation context across multiple messages
- **Foundation Model Support**: Supports multiple AI models (Gemini, OpenAI, Claude, etc.)
- **Dark Mode UI**: Modern, dark-themed responsive interface
- **API Integration**: RESTful backend API with CORS support
- **Easy Setup**: Simple configuration through environment variables

## Project Structure

```
AI Chatbot/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js           # Main app component
│   │   └── index.js         # Entry point
│   ├── public/
│   ├── package.json         # Frontend dependencies
│   └── tailwind.config.js   # Tailwind CSS configuration
│
└── backend/                  # FastAPI backend server
    ├── app/
    │   ├── api/             # API routes and logic
    │   ├── models/          # Data models and schemas
    │   ├── config/          # Configuration settings
    │   └── main.py          # FastAPI app initialization
    ├── requirements.txt     # Python dependencies
    ├── main.py              # Application entry point
    └── .env.example         # Environment variables template
```

## Installation

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the backend server:
```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Configuration

### API Keys

To use the chatbot, you need to configure at least one foundation model API key:

- **Google Gemini**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenAI**: Get your API key from [OpenAI Dashboard](https://platform.openai.com/api-keys)
- **Anthropic Claude**: Get your API key from [Anthropic Console](https://console.anthropic.com/)

Add your API key to the `.env` file:

```env
MODEL_PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Start typing messages in the chat interface
3. The AI will respond based on the selected foundation model
4. The conversation history is maintained within the current session

## API Endpoints

- `POST /api/chat` - Send a message and get a response
- `GET /api/health` - Health check endpoint
- `POST /api/clear` - Clear chat history
- `GET /` - API information

## Technologies Used

### Frontend
- React 18
- Tailwind CSS
- Axios (HTTP client)

### Backend
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (data validation)
- Python-dotenv (environment management)

### AI Models
- Google Gemini
- OpenAI GPT
- Anthropic Claude
- And more...

## Features in Development

- [ ] Voice input/speech recognition
- [ ] User authentication
- [ ] Long-term memory using databases
- [ ] File upload and document Q&A
- [ ] Multilingual support
- [ ] Integration with external tools and APIs
- [ ] Chat persistence and history export

## Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that your `.env` file is properly configured
- Verify the port 8000 is not already in use

### Frontend can't connect to backend
- Ensure the backend is running on `http://localhost:8000`
- Check CORS settings in `backend/app/config/settings.py`
- Verify the API URL in `frontend/src/App.js`

### API Key errors
- Double-check your API key is correctly set in `.env`
- Ensure the API key has the necessary permissions
- Check that you're using the correct MODEL_PROVIDER

## License

MIT License

## Contributing

Feel free to fork, modify, and enhance this project!

## Support

For issues, questions, or suggestions, please open an issue or contact the development team.

---

Happy chatting with your AI! 🤖
