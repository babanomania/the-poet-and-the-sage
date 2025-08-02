This document outlines the setup steps for running the multi-agent system used in **The Poet and the Sage** project. Each agent runs as a separate A2A-compatible microservice and communicates over HTTP.

## Prerequisites

* Python 3.10+
* [uv](https://github.com/astral-sh/uv) (recommended for dependency management)
* `curl` or any HTTP client for testing
* `.env` file configured with appropriate GenAI or VertexAI credentials

---

## 1. Environment Configuration

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

If you're using VertexAI, set `GOOGLE_GENAI_USE_VERTEXAI=TRUE` and ensure the appropriate environment variables for Vertex authentication are also present.

---

## 2. Start Individual Agents

Each agent is hosted independently and must be run in its own terminal window.

### Terminal 1 - Wikipedia Agent
```bash
. .env
cd wikipedia_agent
uv venv
source .venv/bin/activate
uv run --active .
```

### Terminal 2 - Research Agent
```bash
. .env
cd research_agent
uv venv
source .venv/bin/activate
uv run --active .
```

### Terminal 3 - Context Agent
```bash
. .env
cd context_agent
uv venv
source .venv/bin/activate
uv run --active .
```
### Terminal 4 - Poet Agent
```bash
. .env
cd poet_agent
uv venv
source .venv/bin/activate
uv run --active app
```

### Terminal 5 - Critique Agent
```bash
. .env
cd critique_agent
uv venv
source .venv/bin/activate
uv run --active app
```

---

## 3. Start Host Agent

In a separate terminal:

```bash
. .env
cd host_agent
uv venv
source .venv/bin/activate
uv run --active adk web   
```

This host agent connects to the five child agents and exposes a single orchestration endpoint.

### 4. Open the UI
Open the ADK Web Interface at

> http://localhost:8000
