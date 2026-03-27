"""
Gradio frontend — calls the LangServe API and renders responses.
"""

import requests
import gradio as gr

API_URL = "http://localhost:8000/agent/invoke"


def chat_with_agent(user_input: str, history: list):
    """Send a message to the LangServe agent and return its response."""
    if not user_input.strip():
        return history, history

    try:
        payload = {"input": user_input}
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        # LangServe wraps output in {"output": ...}
        answer = data.get("output", "No response received.")
    except requests.exceptions.ConnectionError:
        answer = "❌ Cannot reach the agent server. Make sure `server.py` is running on port 8000."
    except requests.exceptions.Timeout:
        answer = "⏱️ The agent took too long to respond. Try a simpler question."
    except Exception as exc:
        answer = f"⚠️ Unexpected error: {exc}"

    history.append((user_input, answer))
    return history, history


# ── Gradio UI ──────────────────────────────────────────────────────────────────

with gr.Blocks(
    title="LangChain Agent",
    theme=gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="slate",
        font=gr.themes.GoogleFont("IBM Plex Mono"),
    ),
    css="""
        /* ── Global ── */
        body { background: #0d0f1a !important; }

        .gradio-container {
            max-width: 860px !important;
            margin: 0 auto !important;
            font-family: 'IBM Plex Mono', monospace !important;
        }

        /* ── Header ── */
        #header {
            text-align: center;
            padding: 2.5rem 1rem 1.5rem;
            border-bottom: 1px solid #1e2235;
            margin-bottom: 1.5rem;
        }
        #header h1 {
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: #e8eaf6;
            margin: 0 0 0.4rem;
        }
        #header p {
            color: #6c7293;
            font-size: 0.85rem;
            margin: 0;
        }
        .accent { color: #7c83fd; }

        /* ── Chatbot ── */
        #chatbox {
            border: 1px solid #1e2235 !important;
            border-radius: 12px !important;
            background: #10121f !important;
        }
        /* user bubble */
        #chatbox .user > div {
            background: #1e224a !important;
            color: #c5c8f0 !important;
            border-radius: 8px 8px 2px 8px !important;
            font-size: 0.9rem !important;
        }
        /* bot bubble */
        #chatbox .bot > div {
            background: #161824 !important;
            color: #a8accc !important;
            border-radius: 8px 8px 8px 2px !important;
            font-size: 0.9rem !important;
            border: 1px solid #1e2235 !important;
        }

        /* ── Input row ── */
        #input-row { gap: 8px !important; align-items: flex-end !important; }

        #msg-box textarea {
            background: #10121f !important;
            color: #c5c8f0 !important;
            border: 1px solid #1e2235 !important;
            border-radius: 10px !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 0.88rem !important;
            resize: none !important;
        }
        #msg-box textarea:focus {
            border-color: #7c83fd !important;
            box-shadow: 0 0 0 3px rgba(124,131,253,0.12) !important;
        }

        /* ── Buttons ── */
        #send-btn {
            background: #7c83fd !important;
            color: #fff !important;
            border: none !important;
            border-radius: 10px !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            letter-spacing: 0.02em !important;
            transition: background 0.18s, transform 0.1s !important;
        }
        #send-btn:hover {
            background: #5c63d8 !important;
            transform: translateY(-1px) !important;
        }
        #clear-btn {
            background: transparent !important;
            color: #6c7293 !important;
            border: 1px solid #1e2235 !important;
            border-radius: 10px !important;
            font-family: 'IBM Plex Mono', monospace !important;
            font-size: 0.88rem !important;
        }
        #clear-btn:hover { border-color: #7c83fd !important; color: #7c83fd !important; }

        /* ── Status bar ── */
        #status-bar {
            font-size: 0.75rem;
            color: #3d4265;
            text-align: center;
            padding: 0.6rem 0 0;
            border-top: 1px solid #1a1d2e;
            margin-top: 1rem;
        }
        .dot {
            display: inline-block;
            width: 7px; height: 7px;
            background: #4caf82;
            border-radius: 50%;
            margin-right: 5px;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%,100% { opacity: 1; } 50% { opacity: 0.4; }
        }
    """,
) as demo:

    # ── Header ──
    gr.HTML("""
        <div id="header">
            <h1>⬡ <span class="accent">LangChain</span> Agent</h1>
            <p>Zero-shot ReAct agent · powered by GPT-3.5-turbo + LangServe</p>
        </div>
    """)

    # ── Chat window ──
    chatbot = gr.Chatbot(
        elem_id="chatbox",
        label="",
        height=440,
        show_label=False,
        bubble_full_width=False,
    )

    # ── Input row ──
    with gr.Row(elem_id="input-row"):
        msg = gr.Textbox(
            elem_id="msg-box",
            placeholder="Ask me anything — math, search, reasoning…",
            lines=2,
            max_lines=6,
            show_label=False,
            scale=5,
        )
        with gr.Column(scale=1, min_width=110):
            send_btn = gr.Button("Send ↵", elem_id="send-btn", variant="primary")
            clear_btn = gr.Button("Clear", elem_id="clear-btn")

    # ── State ──
    state = gr.State([])

    # ── Events ──
    send_btn.click(
        fn=chat_with_agent,
        inputs=[msg, state],
        outputs=[chatbot, state],
    ).then(fn=lambda: "", outputs=msg)

    msg.submit(
        fn=chat_with_agent,
        inputs=[msg, state],
        outputs=[chatbot, state],
    ).then(fn=lambda: "", outputs=msg)

    clear_btn.click(fn=lambda: ([], []), outputs=[chatbot, state])

    # ── Status bar ──
    gr.HTML("""
        <div id="status-bar">
            <span class="dot"></span>
            Agent API → <code>http://localhost:8000/agent/invoke</code>
            &nbsp;·&nbsp; UI → <code>http://localhost:7860</code>
        </div>
    """)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
