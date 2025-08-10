#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gradio streaming app for a LangGraph chatbot (no structured-output followups).
- Streams assistant tokens in real time
- Preserves full graph state (incl. tool messages)
- Trims history to avoid context bloat
- Uses OpenAI-style messages format in Gradio (type="messages")
"""

from __future__ import annotations
import os
import json
import logging
import logging.config
from uuid import uuid4
from typing import Any

import gradio as gr
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.types import RunnableConfig

# Your graph comes from your own repo
from graph import graph  # noqa: F401

# ------------- Config -------------
TRIM_MESSAGE_LENGTH = 16        # keep last N messages (incl. tool messages)
USER_INPUT_MAX_LENGTH = 10_000  # safety
APP_TITLE = "LangGraph Chatbot — Streaming"

# ------------- Logging -------------
load_dotenv()
if os.path.exists("logging-config.json"):
    try:
        with open("logging-config.json", "r", encoding="utf-8") as fh:
            config = json.load(fh)
        logging.config.dictConfig(config)
    except Exception:
        logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------- Helpers -------------

def ensure_api_key() -> None:
    if not (os.getenv("OPENAI_API_KEY") or os.getenv("MISTRAL_API_KEY")):
        raise RuntimeError(
            "No API key found. Set OPENAI_API_KEY or MISTRAL_API_KEY in your environment/.env."
        )


def _append_and_trim(state: dict[str, Any], message: HumanMessage | AIMessage | SystemMessage) -> None:
    state.setdefault("messages", [])
    state["messages"].append(message)
    state["messages"] = state["messages"][-TRIM_MESSAGE_LENGTH:]


# ------------- Core chat fn (STREAMING) -------------
async def chat_fn(
    user_input: str,
    history_messages: list[dict],
    input_graph_state: dict,
    thread_id: str,
):
    """Streaming handler for Gradio ChatInterface.

    Returns/streams: (assistant_text: str, graph_state: dict)
    """
    try:
        ensure_api_key()

        # Initialize graph state if missing
        if not input_graph_state or "messages" not in input_graph_state:
            input_graph_state = {"messages": [SystemMessage(content="You are a helpful assistant.")]}

        # Add user message to graph state (source of truth)
        text = (user_input or "").strip()
        if not text:
            yield gr.update(), gr.skip()
            return
        _append_and_trim(input_graph_state, HumanMessage(content=text[:USER_INPUT_MAX_LENGTH]))

        # Tell the UI we started processing
        yield "Processing...", gr.skip()

        # Accumulate assistant output as it streams
        output_acc = ""
        final_state: dict[str, Any] | Any = {}
        waiting_output_seq: list[str] = []  # for tool progress banners

        config = RunnableConfig(
            recursion_limit=10,
            run_name="user_chat_stream",
            configurable={"thread_id": thread_id},
        )

        async for stream_mode, chunk in graph.astream(
            input_graph_state,
            config=config,
            stream_mode=["messages"],
        ):
            print(chunk)
            if stream_mode == "values":
                # Updated graph state snapshot
                final_state = chunk
            elif stream_mode == "messages":
                msg, metadata = chunk

                # If the assistant just planned to call tools, show lightweight progress messages
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for call in msg.tool_calls:
                        tool_name = call.get("name") if isinstance(call, dict) else getattr(call, "name", None)
                        if tool_name:
                            # Customize a couple of common tools if you want
                            if tool_name == "download_website_text":
                                waiting_output_seq.append("Downloading website text...")
                            elif tool_name == "tavily_search_results_json":
                                waiting_output_seq.append("Searching for relevant information...")
                            else:
                                waiting_output_seq.append(f"Running {tool_name}...")
                            yield "\n".join(waiting_output_seq), gr.skip()

                # Only stream visible assistant content coming from your assistant node
                node = metadata.get("langgraph_node") if isinstance(metadata, dict) else None
                if node == "model" and getattr(msg, "content", None):
                    output_acc += msg.content
                    yield output_acc, gr.skip()

        # Final push: return last text + final graph state so it persists to next turn
        if isinstance(final_state, dict) and final_state:
            yield output_acc, dict(final_state)
        else:
            # If for some reason we didn't get a values snapshot, return current input_graph_state
            yield output_acc, input_graph_state

    except Exception as e:
        logger.exception("Streaming error")
        yield f"❌ Error: {e}", gr.skip()


# ------------- Clear helpers -------------

def clear_graph_state():
    return dict(messages=[SystemMessage(content="You are a helpful assistant.")]), uuid4().hex[:8]


# ------------- Build UI -------------
if __name__ == "__main__":
    logger.info("Starting streaming interface")

    with gr.Blocks(title=APP_TITLE, fill_height=True) as app:
        # States
        thread_id_state = gr.State(uuid4().hex[:8])
        graph_state = gr.State(dict(messages=[SystemMessage(content="You are a helpful assistant.")]))

        # Chatbot uses OpenAI-style messages
        chatbot = gr.Chatbot(type="messages", height=520)

        # Optional toolbar
        with gr.Row():
            reset_btn = gr.Button("🔄 Reset conversation", variant="secondary")

        # Textbox (single line with submit & stop buttons enabled)
        textbox = gr.Textbox(
            show_label=False,
            placeholder="Ask me anything…",
            autofocus=True,
            submit_btn=True,
            stop_btn=True,
            lines=1,
        )

        # Wire ChatInterface
        chat_ui = gr.ChatInterface(
            chatbot=chatbot,
            fn=chat_fn,
            additional_inputs=[graph_state, thread_id_state],
            additional_outputs=[graph_state],
            type="messages",
            textbox=textbox,
        )

        # Reset clears graph state + assigns a new thread id
        def _on_reset():
            new_state, new_tid = clear_graph_state()
            return new_state, new_tid, []

        reset_btn.click(
            fn=_on_reset,
            inputs=None,
            outputs=[graph_state, thread_id_state, chatbot],
        )

    app.queue().launch(
        server_name="127.0.0.1",
        server_port=7862,
        inbrowser=False,
        show_error=True,
        debug=True,
    )
