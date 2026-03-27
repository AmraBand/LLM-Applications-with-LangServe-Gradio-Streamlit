# ── Stage 1: base ──────────────────────────────────────────────────────────────
FROM python:3.10-slim AS base

# Keep Python output unbuffered so logs stream immediately
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ── Stage 2: dependencies ───────────────────────────────────────────────────────
FROM base AS deps

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 3: runtime ────────────────────────────────────────────────────────────
FROM deps AS runtime

COPY . .

# LangServe API
EXPOSE 8000
# Gradio UI
EXPOSE 7860

# Default: start the API server.
# Override CMD in docker-compose to run the Gradio app in a separate container.
CMD ["python", "server.py"]
