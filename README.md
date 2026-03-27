# ⬡ LangChain Agent · NVIDIA NIM + LangServe + Gradio

A zero-shot ReAct agent powered by **NVIDIA NIM** (OpenAI-compatible API), served via **LangServe** (FastAPI backend), with a **Gradio** chat UI — fully Dockerized.

```
┌────────────────┐  HTTP POST /agent/invoke  ┌───────────────────────────┐
│  Gradio UI     │ ──────────────────────►  │  LangServe (FastAPI)      │
│  :7860         │ ◄──────────────────────  │  :8000                    │
└────────────────┘      JSON response        │  └─ LangChain Agent       │
                                             │     ├─ Tool: SerpAPI      │
                                             │     └─ Tool: llm-math     │
                                             │     └─ LLM: NVIDIA NIM    │
                                             └───────────────────────────┘
```

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.10+ | |
| Docker + Docker Compose | any recent |
| NVIDIA API key | Free at [build.nvidia.com](https://build.nvidia.com) — click any model → "Get API Key" |
| SerpAPI key | [serpapi.com](https://serpapi.com) — free tier available |

---

## Available NVIDIA Models

Set `NVIDIA_MODEL` in your `.env` to any slug from [build.nvidia.com](https://build.nvidia.com):

| Model | Slug |
|-------|------|
| Llama 3.1 70B *(default)* | `meta/llama-3.1-70b-instruct` |
| Llama 3.1 8B | `meta/llama-3.1-8b-instruct` |
| Mixtral 8x7B | `mistralai/mixtral-8x7b-instruct-v0.1` |
| Phi-3 Medium | `microsoft/phi-3-medium-128k-instruct` |
| Gemma 2 27B | `google/gemma-2-27b-it` |

---

## Quick Start (local, no Docker)

```bash
# 1. Clone & enter directory
git clone <repo-url> && cd langchain-agent

# 2. Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env     # edit with your real keys

# 5. Start the API server (terminal 1)
python server.py         # → http://localhost:8000

# 6. Start the Gradio UI (terminal 2)
python app.py            # → http://localhost:7860
```

---

## Quick Start (Docker Compose)

```bash
docker compose up --build

# UI
open http://localhost:7860

# API Swagger playground
open http://localhost:8000/agent/playground
```

Stop everything:
```bash
docker compose down
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent/invoke` | Single synchronous call |
| POST | `/agent/batch` | Batch multiple inputs |
| POST | `/agent/stream` | Streaming (SSE) response |
| GET | `/agent/playground` | Interactive Swagger UI |

**Example cURL:**
```bash
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": "What is 17 * 43?"}'
```

---

## Project Structure

```
langchain-agent/
├── agent.py            # LangChain agent — powered by NVIDIA NIM
├── server.py           # LangServe FastAPI server
├── app.py              # Gradio frontend
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Extending the Agent

**Add more tools** in `agent.py`:
```python
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = load_tools(["serpapi", "llm-math"], llm=llm) + [wiki_tool]
```

**Switch NVIDIA model at runtime** — no code change needed, just update `.env`:
```bash
NVIDIA_MODEL=mistralai/mixtral-8x7b-instruct-v0.1
```
