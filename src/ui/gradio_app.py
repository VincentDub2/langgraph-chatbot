"""
Interface Gradio pour le chatbot
"""
import gradio as gr
from src.graph.builder import graph
from src.core.prompts import prompt_manager


def create_gradio_interface():
    """Crée l'interface Gradio"""
    
    def chat_with_bot(message, history):
        """Fonction de chat avec le bot"""
        try:
            # Préparer les messages pour le graph
            messages = [{"role": "user", "content": message}]
            
            thread_id = 2
            config = {"configurable": {"thread_id": thread_id}}
            # Exécuter le graph
            result = graph.invoke(
                {
                    "messages": messages
                
                },
                 config=config
                 )
            
            # Extraire la réponse
            response_content = ""
            for msg in result["messages"]:
                if hasattr(msg, 'content') and msg.content:
                    response_content += str(msg.content)
            
            return response_content
        except Exception as e:
            return f"Erreur: {str(e)}"

    # Créer l'interface
    interface = gr.ChatInterface(
        fn=chat_with_bot,
        title="Chatbot Agent Immobilier",
        description="Assistant virtuel pour la gestion des rendez-vous immobiliers",
        examples=[
            ["Bonjour, je cherche un appartement à Paris"],
            ["Quels sont les agents disponibles ?"],
            ["Je voudrais prendre un rendez-vous pour visiter un bien"]
        ],
        theme=gr.themes.Soft()
    )
    
    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch()
