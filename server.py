"""
LangServe server — exposes the LangChain agent as a REST API.

Endpoints created automatically by add_routes():
  POST /agent/invoke       — single synchronous call
  POST /agent/batch        — batch calls
  POST /agent/stream       — streaming response
  GET  /agent/playground   — interactive Swagger UI
"""

from fastapi import FastAPI
from langserve import add_routes
from agent import agent

app = FastAPI(
    title="LangChain Agent API",
    description="A LangChain zero-shot-react agent served via LangServe.",
    version="1.0.0",
)

# Mount the agent under /agent
add_routes(app, agent, path="/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
