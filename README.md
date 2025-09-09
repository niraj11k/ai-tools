## Prompt Genie — AI Prompt Generator (FastAPI)

** Prompt Genie is a lightweight FastAPI web app that turns simple ideas into high‑quality, structured prompts you can paste into your favorite LLMs. It supports generating both detailed and short prompts using Together.ai hosted models (Meta Llama, OpenAI, and Gemma). The UI includes a floating assistant (“Vani”) with a basic chatbot flow for prompt improvements and quick actions. ** 

## Features
- Prompt generation: Converts a task description into an optimized prompt.
- Short or detailed: Choose between concise or expanded outputs.
- Multiple providers: Meta‑Llama (Together), Mistral, and Llama‑Vision.
- Clean UI: Tailwind‑styled page with copy‑to‑clipboard.
- Optional chatbot: Floating assistant with simple actions (Improve Prompt, Search, Ask GPT).

## Tech Stack
- Backend: FastAPI, Jinja2 templates, `requests`.
- Models: Together API via `together` SDK and raw HTTP.
- Frontend: TailwindCSS, vanilla JS.

## Project Structure
- app/main.py: FastAPI app, routes for UI and prompt generation.
- app/prompt_generator.py: Provider integrations and prompt logic.
- app/static/main.js: Frontend logic for generate + chatbot.
- app/static/style.css: Styles for the floating chatbot.
- templates/generate_prompt.html: Main page template.
- app/api/chatbot_routes.py: Chat endpoint (see note below to enable).
- app/core/chatbot_handler.py: Chatbot prompt optimization logic.
- app/models/chatbot_models.py: Pydantic models for chat API.

## Getting Started
- Prerequisites: Python 3.10+ and a Together API key.
- Clone: git clone <your-repo-url> && cd ai-tools
- Create venv:
  - Windows: python -m venv venv && .\venv\Scripts\activate
  - macOS/Linux: python -m venv venv && source venv/bin/activate
- Install deps:
  - pip install -r requirements.txt
  - If requirements.txt has encoding issues, install core deps instead: pip install fastapi uvicorn jinja2 python-dotenv requests together markdown-it-py
- Configure env:
  - Create `.env` with your key: TOGETHER_API_KEY=YOUR_KEY
  - Optionally set CORS: ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

## Run The App
- Start server: uvicorn app.main:app --reload
- Open UI: http://localhost:8000

## Dev Container (VS Code / Codespaces)
- Open the repository in VS Code and install the "Dev Containers" extension.
- Reopen in Container. The container exposes port 8000 and installs project deps + pytest.
- Start the app inside the container:
  - uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
- Environment variables: add `.env` in the repo root (loaded by python-dotenv). Alternatively, set `TOGETHER_API_KEY` in the Dev Container environment.

## Testing
- Install pytest: `pip install pytest`
- Run all tests: `pytest -q`
- Run a specific file: `pytest -q tests/test_routes.py`
- Notes: tests mock external API calls, so no network or real API key is required. HTTP-path tests set a dummy `TOGETHER_API_KEY` via monkeypatch.

## Usage
- In the UI, select a provider (Vision, Meta‑Llama, Mistral).
- Enter your task and click “Generate Short Prompt” or “Generate Detailed Prompt”.
- Copy the result and use it in your target LLM.

## HTTP API
- POST /generate
  - Body: { "task": "<your task>", "provider": "vision|together|mistral" }
  - Response: { "prompt": "..." } or { "error": "..." }
- POST /generate-short
  - Body: same as above
  - Response: { "prompt": "..." } or { "error": "..." }

## Chatbot Endpoint (Optional)
- Code for a simple chat endpoint exists at app/api/chatbot_routes.py and logic in app/core/chatbot_handler.py.
- To enable it, include the router in app/main.py:
  - from app.api.chatbot_routes import router as chatbot_router
  - app.include_router(chatbot_router, prefix="/api")
- Frontend sends POST /api/chat with { "message": "..." } and expects { "reply": "..." }.

## Configuration Notes
- CORS: Set ALLOWED_ORIGINS to a comma‑separated list or "*" for all.
- Static files: Served from /static; templates are in /templates.
- Models: This project uses Together‑hosted models. Ensure TOGETHER_API_KEY is valid and has access.

## Troubleshooting
- 401/403 from Together: Verify TOGETHER_API_KEY in .env and that the key is active.
- CORS errors in browser: Set ALLOWED_ORIGINS appropriately or "*" for local dev.
- requirements.txt install issues: Use the fallback install command above.

## License
- MIT (or your preference). Update as needed.
