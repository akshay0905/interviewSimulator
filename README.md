# AI Interview Simulator

An AI-powered technical interview simulation tool built with FastAPI and OpenAI's GPT-4.

## Features

- Start interview sessions with different technical topics
- Get AI-generated interview questions
- Receive detailed feedback on answers
- Text-to-speech support for questions
- Session management with UUIDs
- 10 questions per interview session

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /interview/start
Start a new interview session with a specific topic.

Request:
```json
{
    "topic": "python"  // Options: python, javascript, system_design, algorithms, machine_learning
}
```

### POST /interview/answer
Submit an answer and get feedback + next question.

Request:
```json
{
    "session_id": "uuid",
    "answer": "Your answer here"
}
```

### POST /interview/speak/{session_id}/{question_number}
Get audio version of a specific question.

## Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
