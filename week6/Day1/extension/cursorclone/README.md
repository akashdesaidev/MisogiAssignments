## CursorClone

An experimental VS Code extension that pairs a sidebar chat with a Python LangGraph server to:

- Maintain multi-session chat memory
- Read, search, and write files in the current workspace via safe APIs
- Stream responses from the agent

### Requirements

- Python 3.10+
- A virtualenv at `venv/` with FastAPI and friends (see `requirements.txt`)
- `OPENAI_API_KEY` and optional `TAVILY_API_KEY` in environment or `.env`

### Getting Started

1. Install dependencies: `npm i`
2. Ensure `venv/` exists and `Python/run_server.py` dependencies are installed.
3. Launch the extension (Run Extension) and open the view "CursorClone" in the Activity Bar.

### Features

- New session and session switcher in the sidebar
- Persistent chat history per active session within VS Code global state
- Backend endpoints:
  - POST `/invoke` { input, conversation_id } (stream: ndjson)
  - POST `/clear_history` { conversation_id }
  - POST `/fs/read` { path }
  - POST `/fs/write` { path, content }
  - POST `/fs/search` { path }

### Notes

- The extension passes the workspace root through env `WORKSPACE_ROOT` to the Python server.
