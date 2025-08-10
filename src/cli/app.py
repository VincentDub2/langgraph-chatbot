"""
Interface en ligne de commande pour le chatbot
"""
import os
import sys
import uuid
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.core.config import get_settings
from src.core.prompts import prompt_manager
from src.graph.builder import graph


def ensure_api_key() -> None:
    """Vérifie que les clés API sont configurées"""
    settings = get_settings()
    if not settings.openai_api_key and not settings.mistral_api_key:
        print(
            "Error: OPENAI_API_KEY is not set. Create a .env with OPENAI_API_KEY or export it.",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    """Fonction principale de l'interface CLI"""
    # Charger les variables d'environnement
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    load_dotenv(dotenv_path=env_path, override=False)
    ensure_api_key()

    print("LangGraph Chatbot (type '/quit' to exit, '/new' for new thread, '/thread <id>' to switch)")
    
    # Charger le prompt système
    try:
        system_prompt = prompt_manager.load("chatbot")
    except FileNotFoundError:
        print("Warning: No prompt file found, using default prompt")
        system_prompt = "You are a helpful assistant."
    
    state: dict = {"messages": []}
    initial_messages = [SystemMessage(content=system_prompt)]
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
            thread_id = uuid.uuid4().hex[:8]
            state = {"messages": []}
            initial_messages = [SystemMessage(content=system_prompt)]
            print(f"New thread: {thread_id}")
            continue
        if user_input.startswith("/thread "):
            thread_id = user_input.split(" ", 1)[1].strip() or thread_id
            state = {"messages": []}
            initial_messages = [SystemMessage(content=system_prompt)]
            print(f"Switched to thread: {thread_id}")
            continue

        # Conversation persistante via thread_id dans la config
        state = graph.invoke(
            {"messages": initial_messages + [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": thread_id}},
        )
        initial_messages = []

        ai_messages = [m for m in state["messages"] if isinstance(m, AIMessage)]
        if ai_messages:
            print(f"[{thread_id}] Bot: {ai_messages[-1].content}")
        else:
            print("Bot: (no response)")


if __name__ == "__main__":
    main()
