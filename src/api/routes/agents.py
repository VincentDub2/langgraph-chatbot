"""
Routes de gestion des agents immobiliers
"""
from typing import List
from fastapi import APIRouter, HTTPException

from src.core.models import AgentInfo
from tools import (
    list_agents as list_agents_tool,
    get_agent_info as get_agent_info_tool
)

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("/", response_model=List[AgentInfo])
async def list_agents():
    """
    Lister tous les agents disponibles
    """
    try:
        agents_data = list_agents_tool()
        
        agents = []
        for agent in agents_data:
            agents.append(AgentInfo(
                id=agent["id"],
                name=agent["name"],
                specialities=agent["specialities"],
                languages=agent["languages"]
            ))
        
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des agents: {str(e)}")


@router.get("/{agent_id}", response_model=AgentInfo)
async def get_agent_info(agent_id: str):
    """
    Obtenir les informations détaillées d'un agent
    """
    try:
        agent_data = get_agent_info_tool(agent_id)
        
        if "error" in agent_data:
            raise HTTPException(status_code=404, detail=agent_data["error"])
        
        return AgentInfo(
            id=agent_data["id"],
            name=agent_data["name"],
            specialities=agent_data["specialities"],
            languages=agent_data["languages"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'agent: {str(e)}")
