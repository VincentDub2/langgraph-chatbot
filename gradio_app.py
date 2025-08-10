import os
import uuid
from typing import List, Tuple

import gradio as gr
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from prompt_manager import PromptManager
from graph import graph

# --- Constantes inspirées du snippet GitHub ---
TRIM_MESSAGE_LENGTH = 16       # nombre max de messages gardés côté graph state
USER_INPUT_MAX_LENGTH = 10_000 # sécurité coupe-texte

def ensure_api_key() -> None:
    # message corrigé: accepte OpenAI ou Mistral
    if not (os.getenv("OPENAI_API_KEY") or os.getenv("MISTRAL_API_KEY")):
        raise ValueError(
            "Error: no API key set. Create a .env with OPENAI_API_KEY or MISTRAL_API_KEY."
        )

class ChatbotInterface:
    def __init__(self):
        # Load environment variables
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path=env_path, override=False)
        ensure_api_key()

        # Initialize prompt manager and system prompt
        self.pm = PromptManager()
        self.system_prompt = self.pm.load("chatbot")

        # Initialize state
        self.thread_id = uuid.uuid4().hex[:8]
        # IMPORTANT: on garde un graph_state qui contiendra aussi les ToolMessages
        self.graph_state = {"messages": [SystemMessage(content=self.system_prompt)]}
        self.chat_history = []  # seulement pour affichage gradio

    def reset_chat(self):
        """Reset the chat to start a new conversation"""
        self.thread_id = uuid.uuid4().hex[:8]
        self.graph_state = {"messages": [SystemMessage(content=self.system_prompt)]}
        self.chat_history = []
        return [], f"🆕 Nouvelle conversation créée (Thread: {self.thread_id})"

    def _trim_graph_messages(self):
        # garde seulement les N derniers messages (incl. tool messages si ton graph les ajoute)
        if "messages" in self.graph_state:
            self.graph_state["messages"] = self.graph_state["messages"][-TRIM_MESSAGE_LENGTH:]

    def send_message(self, message: str, history_messages: List[dict]) -> Tuple[List[dict], str]:
        """
        Gradio Chatbot en mode type='messages'
        - history_messages est une liste de dicts {'role','content'}
        - on n'utilise PAS cette history pour le LLM (on passe par self.graph_state)
        """
        msg = (message or "").strip()
        if not msg:
            return history_messages, ""

        # 1) Affichage: pousser le message user dans l'historique UI
        history_messages.append({"role": "user", "content": msg})

        try:
            # 2) Alimente l'état du graphe (source de vérité)
            self.graph_state.setdefault("messages", [])
            self.graph_state["messages"].append(HumanMessage(content=msg[:USER_INPUT_MAX_LENGTH]))
            self._trim_graph_messages()

            # 3) Appel du graph (non-streamé pour rester simple)
            self.graph_state = graph.invoke(
                self.graph_state,
                config={"configurable": {"thread_id": self.thread_id}, "run_name": "user_chat"},
            )

            # 4) Récupère la dernière réponse AI
            ai_messages = [m for m in self.graph_state.get("messages", []) if isinstance(m, AIMessage)]
            if ai_messages:
                response = ai_messages[-1].content
                history_messages.append({"role": "assistant", "content": response})
                return history_messages, ""
            else:
                history_messages.append({"role": "assistant", "content": "❌ Aucune réponse reçue"})
                return history_messages, ""

        except Exception as e:
            history_messages.append({"role": "assistant", "content": f"❌ Erreur: {e}"})
            return history_messages, ""

    def get_thread_info(self) -> str:
        return f"Thread actuel: {self.thread_id}"

def create_interface():
    bot = ChatbotInterface()

    with gr.Blocks(title="LangGraph Chatbot", theme=gr.themes.Soft()) as interface:
        gr.Markdown(
            """
            # 🤖 LangGraph Chatbot

            Un chatbot intelligent basé sur LangGraph avec outils intégrés (calculs, disponibilité, temps, web).
            """
        )

        with gr.Row():
            with gr.Column(scale=3):
                # IMPORTANT: type='messages' (openai-style)
                chatbot_component = gr.Chatbot(
                    label="Conversation",
                    height=500,
                    show_label=True,
                    container=True,
                    bubble_full_width=False,
                    type="messages",
                    value=[],  # évite le warning d’initialisation
                )

                with gr.Row():
                    message_input = gr.Textbox(
                        label="Votre message",
                        placeholder="Tapez votre message ici...",
                        lines=2,
                        scale=4,
                    )
                    send_button = gr.Button("Envoyer", variant="primary", scale=1)

                with gr.Row():
                    clear_button = gr.Button("🔄 Nouvelle conversation", variant="secondary")
                    thread_info = gr.Textbox(
                        label="Informations du thread",
                        value=bot.get_thread_info(),
                        interactive=False,
                    )

            with gr.Column(scale=1):
                gr.Markdown("### 📋 Aide")
                gr.Markdown(
                    """
                    **Conseils**  
                    - L'historique est géré côté agent (préserve les ToolMessages).
                    - Seuls les ~16 derniers messages sont gardés pour limiter le contexte.
                    """
                )

        # Event handlers
        def send_message_wrapper(message, history_messages):
            return bot.send_message(message, history_messages)

        def reset_chat_wrapper():
            history, _ = bot.reset_chat()
            return history, bot.get_thread_info()

        # Connect events
        send_button.click(
            fn=send_message_wrapper,
            inputs=[message_input, chatbot_component],
            outputs=[chatbot_component, message_input],
        )
        message_input.submit(
            fn=send_message_wrapper,
            inputs=[message_input, chatbot_component],
            outputs=[chatbot_component, message_input],
        )
        clear_button.click(
            fn=reset_chat_wrapper,
            outputs=[chatbot_component, thread_info],
        )

    return interface

if __name__ == "__main__":
    ui = create_interface()
    # queue() pour éviter les appels concurrents
    ui.queue().launch(
        server_name="127.0.0.1",  # évite l’onglet about:blank sur certains browsers
        server_port=7861,
        share=False,              # passe à True si tu veux un lien public
        show_error=True,
        debug=True,
        inbrowser=False,          # ouvre l’URL toi-même
    )
