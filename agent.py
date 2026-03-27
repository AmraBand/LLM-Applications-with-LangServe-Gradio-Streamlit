from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, load_tools
import os

# ── NVIDIA NIM configuration ───────────────────────────────────────────────────
# NVIDIA's inference API is OpenAI-compatible; we just point the base_url at
# their endpoint and pass the NVIDIA API key as the openai_api_key parameter.
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Choose any model available on NVIDIA NIM:
#   meta/llama-3.1-70b-instruct  (recommended — strong reasoning)
#   mistralai/mixtral-8x7b-instruct-v0.1
#   microsoft/phi-3-medium-128k-instruct
#   google/gemma-2-27b-it
NVIDIA_MODEL = os.environ.get("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct")


def create_agent():
    """Create and return a LangChain agent backed by NVIDIA NIM."""
    llm = ChatOpenAI(
        model=NVIDIA_MODEL,
        base_url=NVIDIA_BASE_URL,
        api_key=os.environ.get("NVIDIA_API_KEY"),   # nvapi-...
        temperature=0,
        max_tokens=1024,
    )

    # Load SerpAPI only when a key is provided so local startup works with NIM alone.
    tool_names = ["llm-math"]
    if os.environ.get("SERPAPI_API_KEY"):
        tool_names.insert(0, "serpapi")
    tools = load_tools(tool_names, llm=llm)

    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent


# Singleton agent instance used by the server
agent = create_agent()
