from __future__ import annotations
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class AgentInfo:
    id: str
    name: str
    email: str
    phone: str
    specialities: List[str]
    languages: List[str]
    working_hours: Dict[str, List[str]]
    description: str

# Base de données des agents (simulée)
AGENTS_DB = {
    "agent1": AgentInfo(
        id="agent1",
        name="Marie Dubois",
        email="marie.dubois@agence-immobiliere.fr",
        phone="+33 1 23 45 67 89",
        specialities=["Appartements", "Maisons", "Investissement locatif"],
        languages=["Français", "Anglais"],
        working_hours={
            "monday": ["09:00-12:00", "14:00-18:00"],
            "tuesday": ["09:00-12:00", "14:00-18:00"],
            "wednesday": ["09:00-12:00", "14:00-18:00"],
            "thursday": ["09:00-12:00", "14:00-18:00"],
            "friday": ["09:00-12:00", "14:00-18:00"],
            "saturday": ["09:00-12:00"],
            "sunday": []
        },
        description="Spécialiste des biens familiaux et investissement locatif. Plus de 10 ans d'expérience."
    ),
    "agent2": AgentInfo(
        id="agent2",
        name="Pierre Martin",
        email="pierre.martin@agence-immobiliere.fr",
        phone="+33 1 23 45 67 90",
        specialities=["Bureaux", "Locaux commerciaux", "Terrains"],
        languages=["Français", "Espagnol"],
        working_hours={
            "monday": ["09:00-12:00", "14:00-18:00"],
            "tuesday": ["09:00-12:00", "14:00-18:00"],
            "wednesday": ["09:00-12:00", "14:00-18:00"],
            "thursday": ["09:00-12:00", "14:00-18:00"],
            "friday": ["09:00-12:00", "14:00-18:00"],
            "saturday": [],
            "sunday": []
        },
        description="Expert en immobilier commercial et bureaux. Spécialiste des transactions B2B."
    ),
    "agent3": AgentInfo(
        id="agent3",
        name="Sophie Bernard",
        email="sophie.bernard@agence-immobiliere.fr",
        phone="+33 1 23 45 67 91",
        specialities=["Luxury", "Villas", "Penthouses", "International"],
        languages=["Français", "Anglais", "Italien"],
        working_hours={
            "monday": ["09:00-12:00", "14:00-18:00"],
            "tuesday": ["09:00-12:00", "14:00-18:00"],
            "wednesday": ["09:00-12:00", "14:00-18:00"],
            "thursday": ["09:00-12:00", "14:00-18:00"],
            "friday": ["09:00-12:00", "14:00-18:00"],
            "saturday": ["10:00-16:00"],
            "sunday": []
        },
        description="Spécialiste du marché de luxe et clientèle internationale. Plus de 15 ans d'expérience."
    )
}

def get_agent_info(agent_id: str) -> Dict:
    """
    Récupère les informations détaillées d'un agent immobilier.
    
    Args:
        agent_id: Identifiant de l'agent (agent1, agent2, agent3)
    
    Returns:
        Dictionnaire avec les informations de l'agent
    """
    if agent_id not in AGENTS_DB:
        return {"error": f"Agent {agent_id} non trouvé"}
    
    agent = AGENTS_DB[agent_id]
    return {
        "id": agent.id,
        "name": agent.name,
        "email": agent.email,
        "phone": agent.phone,
        "specialities": agent.specialities,
        "languages": agent.languages,
        "working_hours": agent.working_hours,
        "description": agent.description
    }

def list_agents() -> List[Dict]:
    """
    Liste tous les agents disponibles avec leurs informations de base.
    
    Returns:
        Liste des agents avec leurs informations essentielles
    """
    agents = []
    for agent_id, agent in AGENTS_DB.items():
        agents.append({
            "id": agent.id,
            "name": agent.name,
            "specialities": agent.specialities,
            "languages": agent.languages,
            "description": agent.description
        })
    return agents

def find_agent_by_speciality(speciality: str) -> List[Dict]:
    """
    Trouve les agents spécialisés dans un domaine particulier.
    
    Args:
        speciality: Spécialité recherchée (ex: "Appartements", "Luxury", "Bureaux")
    
    Returns:
        Liste des agents correspondants
    """
    matching_agents = []
    for agent_id, agent in AGENTS_DB.items():
        if speciality.lower() in [s.lower() for s in agent.specialities]:
            matching_agents.append({
                "id": agent.id,
                "name": agent.name,
                "specialities": agent.specialities,
                "description": agent.description
            })
    return matching_agents

def get_agent_availability_summary(agent_id: str) -> Dict:
    """
    Récupère un résumé des disponibilités d'un agent.
    
    Args:
        agent_id: Identifiant de l'agent
    
    Returns:
        Résumé des horaires de travail
    """
    if agent_id not in AGENTS_DB:
        return {"error": f"Agent {agent_id} non trouvé"}
    
    agent = AGENTS_DB[agent_id]
    return {
        "agent_id": agent.id,
        "name": agent.name,
        "working_days": list(agent.working_hours.keys()),
        "hours_per_day": agent.working_hours,
        "weekend_available": bool(agent.working_hours.get("saturday", []))
    }
