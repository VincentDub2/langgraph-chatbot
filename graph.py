import json
import os
from re import M
import os
from typing import Annotated, Dict, List, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool as lc_tool
from langchain_core.messages import SystemMessage

from tools import (
    calculate_expression, 
    fetch_url, 
    get_current_time, 
    check_availability as check_availability_tool, 
    create_event as create_event_tool,
    get_agent_info as get_agent_info_tool,
    list_agents as list_agents_tool,
    find_agent_by_speciality as find_agent_by_speciality_tool,
    get_agent_availability_summary as get_agent_availability_summary_tool,
    validate_client_data as validate_client_data_tool,
    create_client_info as create_client_info_tool,
    suggest_agent_by_preferences as suggest_agent_by_preferences_tool,
    format_client_summary as format_client_summary_tool,
    get_property_info as get_property_info_tool,
    list_properties as list_properties_tool,
    search_properties_by_criteria as search_properties_by_criteria_tool,
    get_properties_by_agent as get_properties_by_agent_tool,
    get_property_summary as get_property_summary_tool,
    suggest_properties_for_client as suggest_properties_for_client_tool
)
from prompt_manager import load_system_prompt, get_default_system_prompt


class ChatState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


# Wrap plain functions as LangChain Tools so the model can call them
@lc_tool
def calc(expression: str) -> str:
    """Evaluate a math expression. Use for arithmetic like 2*(3+4)."""
    return calculate_expression(expression)


@lc_tool
def check_availability(agent_id: str, window: str) -> str:
    """
    Retourne un JSON stringifié de slots triés (is_available True/False).
    Exemple d'entrée: "today", "tomorrow afternoon", "next 7 days", "2025-08-12 morning"
    """
    data = check_availability_tool(agent_id, window)
    return json.dumps(data, ensure_ascii=False)

@lc_tool
def create_event(agent_id: str, start: str, end: str, title: str, attendees: str = None, location: str = None, description: str = None) -> str:
    """
    Crée un événement de rendez-vous immobilier.
    
    Args:
        agent_id: Identifiant de l'agent (ex: "agent1", "agent2")
        start: Date/heure de début (format ISO: "2025-01-15T14:00:00")
        end: Date/heure de fin (format ISO: "2025-01-15T15:00:00")
        title: Titre du rendez-vous
        attendees: JSON string des participants [{"name": "John Doe", "email": "john@example.com"}]
        location: Adresse du bien à visiter
        description: Description du rendez-vous
    
    Returns:
        JSON string avec les détails de l'événement créé
    """
    try:
        # Parse attendees if provided
        attendees_list = None
        if attendees:
            attendees_list = json.loads(attendees)
        
        data = create_event_tool(
            agent_id=agent_id,
            start=start,
            end=end,
            title=title,
            attendees=attendees_list,
            location=location,
            description=description
        )
        return json.dumps(data, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@lc_tool
def get_agent_info(agent_id: str) -> str:
    """
    Récupère les informations détaillées d'un agent immobilier.
    
    Args:
        agent_id: Identifiant de l'agent (agent1, agent2, agent3)
    
    Returns:
        JSON string avec les informations de l'agent
    """
    data = get_agent_info_tool(agent_id)
    return json.dumps(data, ensure_ascii=False)

@lc_tool
def list_agents() -> str:
    """
    Liste tous les agents disponibles avec leurs informations de base.
    
    Returns:
        JSON string avec la liste des agents
    """
    data = list_agents_tool()
    return json.dumps(data, ensure_ascii=False)

@lc_tool
def find_agent_by_speciality(speciality: str) -> str:
    """
    Trouve les agents spécialisés dans un domaine particulier.
    
    Args:
        speciality: Spécialité recherchée (ex: "Appartements", "Luxury", "Bureaux")
    
    Returns:
        JSON string avec la liste des agents correspondants
    """
    data = find_agent_by_speciality_tool(speciality)
    return json.dumps(data, ensure_ascii=False)

@lc_tool
def get_agent_availability_summary(agent_id: str) -> str:
    """
    Récupère un résumé des disponibilités d'un agent.
    
    Args:
        agent_id: Identifiant de l'agent
    
    Returns:
        JSON string avec le résumé des horaires de travail
    """
    data = get_agent_availability_summary_tool(agent_id)
    return json.dumps(data, ensure_ascii=False)

@lc_tool
def validate_client_data(client_data: str) -> str:
    """
    Valide les données client (nom, email, téléphone, etc.).
    
    Args:
        client_data: JSON string avec les données client
    
    Returns:
        JSON string avec le résultat de la validation
    """
    try:
        data = json.loads(client_data)
        is_valid, errors = validate_client_data_tool(data)
        return json.dumps({
            "is_valid": is_valid,
            "errors": errors
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@lc_tool
def suggest_agent_by_preferences(client_data: str) -> str:
    """
    Suggère un agent basé sur les préférences du client.
    
    Args:
        client_data: JSON string avec les données client
    
    Returns:
        JSON string avec l'agent suggéré
    """
    try:
        data = json.loads(client_data)
        suggested_agent = suggest_agent_by_preferences_tool(data)
        return json.dumps({
            "suggested_agent": suggested_agent
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@lc_tool
def get_property_info(property_id: str) -> str:
    """
    Récupère les informations détaillées d'une propriété.
    
    Args:
        property_id: Identifiant de la propriété (prop1, prop2, etc.)
    
    Returns:
        JSON string avec les informations de la propriété
    """
    data = get_property_info_tool(property_id)
    return json.dumps(data, ensure_ascii=False)

@lc_tool
def list_properties(property_type: str = None, max_price: str = None, location: str = None) -> str:
    """
    Liste les propriétés avec filtres optionnels.
    
    Args:
        property_type: Type de propriété (Appartement, Maison, Bureau, etc.)
        max_price: Prix maximum (en euros)
        location: Localisation recherchée
    
    Returns:
        JSON string avec la liste des propriétés
    """
    try:
        max_price_float = float(max_price) if max_price else None
        data = list_properties_tool(property_type, max_price_float, location)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@lc_tool
def search_properties_by_criteria(criteria: str) -> str:
    """
    Recherche avancée de propriétés selon plusieurs critères.
    
    Args:
        criteria: JSON string avec les critères de recherche
    
    Returns:
        JSON string avec la liste des propriétés correspondantes
    """
    try:
        criteria_dict = json.loads(criteria)
        data = search_properties_by_criteria_tool(criteria_dict)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@lc_tool
def get_properties_by_agent(agent_id: str) -> str:
    """
    Récupère toutes les propriétés gérées par un agent.
    
    Args:
        agent_id: Identifiant de l'agent
    
    Returns:
        JSON string avec la liste des propriétés de l'agent
    """
    data = get_properties_by_agent_tool(agent_id)
    return json.dumps(data, ensure_ascii=False)

@lc_tool
def get_property_summary(property_id: str) -> str:
    """
    Génère un résumé formaté d'une propriété.
    
    Args:
        property_id: Identifiant de la propriété
    
    Returns:
        Résumé formaté de la propriété
    """
    summary = get_property_summary_tool(property_id)
    return summary

@lc_tool
def suggest_properties_for_client(client_preferences: str) -> str:
    """
    Suggère des propriétés basées sur les préférences client.
    
    Args:
        client_preferences: JSON string avec les préférences du client
    
    Returns:
        JSON string avec la liste des propriétés suggérées
    """
    try:
        preferences_dict = json.loads(client_preferences)
        data = suggest_properties_for_client_tool(preferences_dict)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@lc_tool
def now() -> str:
    """Get the current UTC time in ISO 8601 format."""
    return get_current_time()


TOOLS = [
    calc, 
    check_availability, 
    create_event, 
    get_agent_info,
    list_agents,
    find_agent_by_speciality,
    get_agent_availability_summary,
    validate_client_data,
    suggest_agent_by_preferences,
    get_property_info,
    list_properties,
    search_properties_by_criteria,
    get_properties_by_agent,
    get_property_summary,
    suggest_properties_for_client,
    now
]
tool_node = ToolNode(TOOLS)


def call_model(state: ChatState) -> dict:
    # Bind tools so the model can decide to call them via function/tool calls

    model = ChatOpenAI(
        model="gpt-oss-120b",
        temperature=0.2,
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
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
    last = state["messages"][-1]
    # If the model requested any tool calls, go to the tools node; otherwise end
    if getattr(last, "tool_calls", None):
        return "tools"
    return END


def create_graph():
    builder = StateGraph(ChatState)
    builder.add_node("model", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "model")
    builder.add_conditional_edges(
        "model",
        route_tools,
        {"tools": "tools", END: END},
    )
    # After tools run, go back to the model to incorporate tool results
    builder.add_edge("tools", "model")
    # Persistent across invocations via thread_id within process lifetime
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


graph = create_graph()


