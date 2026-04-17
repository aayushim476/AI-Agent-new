# AI Agent - FastAPI + MongoDB

Multi-tool AI agent with JWT authentication and a beautiful UI.

## Project Structure

```
ai_agent/
├── main.py               # FastAPI app entry point
├── config.py             # Environment config
├── database.py           # MongoDB connection
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (edit this!)
├── models/
│   ├── user.py           # User Pydantic models
│   └── task.py           # Task Pydantic models
├── routes/
│   ├── auth.py           # Register, Login endpoints
│   └── agent.py          # Agent run, history endpoints
├── tools/
│   ├── text_gen.py       # Text generation (OpenAI GPT)
│   ├── image_gen.py      # Image generation (DALL-E)
│   ├── chat.py           # General chat handler
│   └── task_agent.py     # Multi-step task agent
├── utils/
│   ├── auth_utils.py     # JWT + password hashing
│   └── tool_router.py    # Query → tool routing logic
└── static/
    └── index.html        # Full frontend UI
```

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure .env
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=ai_agent_db
SECRET_KEY=your-super-secret-key
OPENAI_API_KEY=your-openai-api-key
```

### 3. Start MongoDB
```bash
# macOS
brew services start mongodb-community

# Ubuntu/Linux
sudo systemctl start mongod

# Docker
docker run -d -p 27017:27017 mongo
```

### 4. Run the server
```bash
cd ai_agent
uvicorn main:app --reload --port 8000
```

### 5. Open the UI
Visit: http://localhost:8000

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/register | No | Register new user |
| POST | /auth/login | No | Login, get JWT token |
| POST | /agent/run | Yes | Run AI agent |
| GET | /agent/history | Yes | Get task history |
| DELETE | /agent/history | Yes | Clear task history |
| GET | /health | No | Health check |
| GET | /docs | No | Swagger UI |

## Tool Routing Logic

The `tool_router.py` uses keyword matching:
- **text_generator**: write, blog, essay, summarize, explain, article
- **image_generator**: generate image, draw, picture of, image of
- **task_agent**: "and also", "both", "as well as" (multi-step)
- **chat_handler**: everything else (default)

## Technologies

- **FastAPI** - Web framework
- **MongoDB + Motor** - Async database
- **JWT (python-jose)** - Authentication tokens
- **Passlib + bcrypt** - Password hashing
- **OpenAI** - GPT-3.5 + DALL-E 3
