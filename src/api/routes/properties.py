"""
Routes de gestion des propriétés immobilières
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException

from src.core.models import PropertyInfo, SearchCriteria, SearchResponse
from tools import (
    list_properties as list_properties_tool,
    get_property_info as get_property_info_tool,
    search_properties_by_criteria as search_properties_by_criteria_tool
)

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get("/", response_model=List[PropertyInfo])
async def list_properties(
    property_type: Optional[str] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None
):
    """
    Lister les propriétés avec filtres optionnels
    """
    try:
        properties_data = list_properties_tool(property_type, max_price, location)
        
        properties = []
        for prop in properties_data:
            properties.append(PropertyInfo(
                id=prop["id"],
                title=prop["title"],
                type=prop["type"],
                price=prop["price"],
                location=prop["location"],
                surface=prop["surface"],
                rooms=prop["rooms"],
                bedrooms=prop["bedrooms"]
            ))
        
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des propriétés: {str(e)}")


@router.get("/{property_id}", response_model=PropertyInfo)
async def get_property_info(property_id: str):
    """
    Obtenir les informations détaillées d'une propriété
    """
    try:
        property_data = get_property_info_tool(property_id)
        
        if "error" in property_data:
            raise HTTPException(status_code=404, detail=property_data["error"])
        
        return PropertyInfo(
            id=property_data["id"],
            title=property_data["title"],
            type=property_data["type"],
            price=property_data["price"],
            location=property_data["location"],
            surface=property_data["surface"],
            rooms=property_data["rooms"],
            bedrooms=property_data["bedrooms"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de la propriété: {str(e)}")


@router.get("/search", response_model=SearchResponse)
async def search_properties(
    type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_surface: Optional[float] = None,
    max_surface: Optional[float] = None,
    min_bedrooms: Optional[int] = None,
    location: Optional[str] = None,
    agent_id: Optional[str] = None
):
    """
    Recherche avancée de propriétés
    """
    try:
        criteria = {}
        if type:
            criteria["type"] = type
        if min_price:
            criteria["min_price"] = min_price
        if max_price:
            criteria["max_price"] = max_price
        if min_surface:
            criteria["min_surface"] = min_surface
        if max_surface:
            criteria["max_surface"] = max_surface
        if min_bedrooms:
            criteria["min_bedrooms"] = min_bedrooms
        if location:
            criteria["location"] = location
        if agent_id:
            criteria["agent_id"] = agent_id
        
        properties_data = search_properties_by_criteria_tool(criteria)
        
        properties = []
        for prop in properties_data:
            properties.append(PropertyInfo(
                id=prop["id"],
                title=prop["title"],
                type=prop["type"],
                price=prop["price"],
                location=prop["location"],
                surface=prop["surface"],
                rooms=prop["rooms"],
                bedrooms=prop["bedrooms"]
            ))
        
        return SearchResponse(
            criteria=criteria,
            count=len(properties),
            properties=properties
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {str(e)}")
