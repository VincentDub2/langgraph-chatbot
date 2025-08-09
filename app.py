import os
import sys

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from graph import graph


def ensure_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("MISTRAL_API_KEY"):
        print(
            "Error: OPENAI_API_KEY is not set. Create a .env with OPENAI_API_KEY or export it.",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    # Explicit path avoids python-dotenv introspection issues on some Python versions
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path, override=False)
    ensure_api_key()

    print("LangGraph Chatbot (type '/quit' to exit, '/new' for new thread, '/thread <id>' to switch)")
    state = {"messages": []}
    thread_id = "default"

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input in {"/quit", "/exit"}:
            break
        if user_input == "/new":
            import uuid
            thread_id = uuid.uuid4().hex[:8]
            state = {"messages": []}
            print(f"New thread: {thread_id}")
            continue
        if user_input.startswith("/thread "):
            thread_id = user_input.split(" ", 1)[1].strip() or thread_id
            state = {"messages": []}
            print(f"Switched to thread: {thread_id}")
            continue

        # Persisted conversation via thread_id in config
        state = graph.invoke(
            {**state, "messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": thread_id}},
        )

        ai_messages = [m for m in state["messages"] if isinstance(m, AIMessage)]
        if ai_messages:
            print(f"[{thread_id}] Bot: {ai_messages[-1].content}")
        else:
            print("Bot: (no response)")


if __name__ == "__main__":
    main()


