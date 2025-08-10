"""
Construction du graphe LangGraph
"""
import os
from typing import Annotated, Dict, List, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from src.core.config import get_settings
from src.core.prompts import load_system_prompt, get_default_system_prompt
from src.graph.tools import TOOLS


class ChatState(TypedDict):
    """État du chat"""
    messages: Annotated[List[AnyMessage], add_messages]


def call_model(state: ChatState) -> dict:
    """Appelle le modèle de langage avec les outils"""
    settings = get_settings()
    
    print(settings.api_key)

    model = ChatOpenAI(
        model=settings.model_name,
        temperature=settings.temperature,
        api_key=settings.api_key,
        base_url=settings.base_url,
    ).bind_tools(TOOLS)

    # Charger le prompt système
    system_prompt = load_system_prompt("v1")
    if not system_prompt:
        system_prompt = get_default_system_prompt()
    
    # Ajouter le message système au début si pas déjà présent
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=system_prompt)] + messages
    
    response = model.invoke(messages)
    print(response)
    return {"messages": [response]}


def route_tools(state: ChatState):
    """Route vers les outils ou fin selon les appels d'outils"""
    last = state["messages"][-1]
    # Si le modèle a demandé des appels d'outils, aller vers le nœud outils
    if getattr(last, "tool_calls", None):
        return "tools"
    return END


def create_graph():
    """Crée et compile le graphe LangGraph"""
    builder = StateGraph(ChatState)
    
    # Créer le nœud d'outils
    tool_node = ToolNode(TOOLS)
    
    # Ajouter les nœuds
    builder.add_node("model", call_model)
    builder.add_node("tools", tool_node)
    
    # Ajouter les arêtes
    builder.add_edge(START, "model")
    builder.add_conditional_edges(
        "model",
        route_tools,
        {"tools": "tools", END: END},
    )
    # Après l'exécution des outils, retourner au modèle
    builder.add_edge("tools", "model")
    
    # Persistance via thread_id
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


# Instance globale du graphe
graph = create_graph()
