from __future__ import annotations
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
from datetime import datetime

@dataclass
class PropertyInfo:
    id: str
    title: str
    type: str
    price: float
    location: str
    surface: float
    rooms: int
    bedrooms: int
    description: str
    features: List[str]
    available_for_visit: bool
    agent_id: str
    images: List[str]
    created_date: str

# Base de données des propriétés (simulée)
PROPERTIES_DB = {
    "prop1": PropertyInfo(
        id="prop1",
        title="Appartement T3 moderne - Quartier Latin",
        type="Appartement",
        price=450000,
        location="5ème arrondissement, Paris",
        surface=65.0,
        rooms=3,
        bedrooms=2,
        description="Magnifique appartement rénové avec goût, situé dans le cœur historique du Quartier Latin. Proche des transports et commerces.",
        features=["Balcon", "Ascenseur", "Cave", "Double vitrage", "Chauffage électrique"],
        available_for_visit=True,
        agent_id="agent1",
        images=["prop1_img1.jpg", "prop1_img2.jpg"],
        created_date="2025-01-10"
    ),
    "prop2": PropertyInfo(
        id="prop2",
        title="Maison familiale avec jardin - Neuilly-sur-Seine",
        type="Maison",
        price=1200000,
        location="Neuilly-sur-Seine, 92",
        surface=180.0,
        rooms=5,
        bedrooms=4,
        description="Belle maison familiale avec jardin paysager, garage et terrasse. Idéale pour une famille avec enfants.",
        features=["Jardin", "Garage", "Terrasse", "Cheminée", "Cuisine équipée"],
        available_for_visit=True,
        agent_id="agent1",
        images=["prop2_img1.jpg", "prop2_img2.jpg"],
        created_date="2025-01-08"
    ),
    "prop3": PropertyInfo(
        id="prop3",
        title="Bureau 200m² - La Défense",
        type="Bureau",
        price=850000,
        location="La Défense, 92",
        surface=200.0,
        rooms=1,
        bedrooms=0,
        description="Bureau moderne dans un immeuble de standing à La Défense. Idéal pour entreprise en croissance.",
        features=["Climatisation", "Ascenseur", "Sécurité 24h", "Parking", "Vue dégagée"],
        available_for_visit=True,
        agent_id="agent2",
        images=["prop3_img1.jpg"],
        created_date="2025-01-05"
    ),
    "prop4": PropertyInfo(
        id="prop4",
        title="Local commercial 150m² - Champs-Élysées",
        type="Local commercial",
        price=2500000,
        location="8ème arrondissement, Paris",
        surface=150.0,
        rooms=1,
        bedrooms=0,
        description="Local commercial prestigieux sur les Champs-Élysées. Parfait pour boutique de luxe ou restaurant.",
        features=["Vitrine", "Cave", "Mezzanine", "Climatisation", "Sécurité"],
        available_for_visit=True,
        agent_id="agent2",
        images=["prop4_img1.jpg", "prop4_img2.jpg"],
        created_date="2025-01-03"
    ),
    "prop5": PropertyInfo(
        id="prop5",
        title="Penthouse de luxe - 16ème arrondissement",
        type="Penthouse",
        price=3500000,
        location="16ème arrondissement, Paris",
        surface=250.0,
        rooms=6,
        bedrooms=4,
        description="Penthouse exceptionnel avec vue panoramique sur Paris. Finitions de luxe et équipements haut de gamme.",
        features=["Terrasse", "Piscine", "Ascenseur privatif", "Domotique", "Conciergerie"],
        available_for_visit=True,
        agent_id="agent3",
        images=["prop5_img1.jpg", "prop5_img2.jpg", "prop5_img3.jpg"],
        created_date="2025-01-01"
    ),
    "prop6": PropertyInfo(
        id="prop6",
        title="Villa de prestige - Saint-Tropez",
        type="Villa",
        price=8500000,
        location="Saint-Tropez, 83",
        surface=400.0,
        rooms=8,
        bedrooms=6,
        description="Villa de prestige avec vue mer, piscine à débordement et accès direct à la plage. Idéale pour investissement ou résidence principale.",
        features=["Piscine", "Vue mer", "Plage privée", "Héliport", "Spa"],
        available_for_visit=True,
        agent_id="agent3",
        images=["prop6_img1.jpg", "prop6_img2.jpg"],
        created_date="2024-12-28"
    )
}

def get_property_info(property_id: str) -> Dict:
    """
    Récupère les informations détaillées d'une propriété.
    
    Args:
        property_id: Identifiant de la propriété
    
    Returns:
        Dictionnaire avec les informations de la propriété
    """
    if property_id not in PROPERTIES_DB:
        return {"error": f"Propriété {property_id} non trouvée"}
    
    prop = PROPERTIES_DB[property_id]
    return {
        "id": prop.id,
        "title": prop.title,
        "type": prop.type,
        "price": prop.price,
        "location": prop.location,
        "surface": prop.surface,
        "rooms": prop.rooms,
        "bedrooms": prop.bedrooms,
        "description": prop.description,
        "features": prop.features,
        "available_for_visit": prop.available_for_visit,
        "agent_id": prop.agent_id,
        "images": prop.images,
        "created_date": prop.created_date
    }

def list_properties(property_type: Optional[str] = None, max_price: Optional[float] = None, location: Optional[str] = None) -> List[Dict]:
    """
    Liste les propriétés avec filtres optionnels.
    
    Args:
        property_type: Type de propriété (Appartement, Maison, Bureau, etc.)
        max_price: Prix maximum
        location: Localisation recherchée
    
    Returns:
        Liste des propriétés correspondant aux critères
    """
    properties = []
    
    for prop_id, prop in PROPERTIES_DB.items():
        # Filtres
        if property_type and prop.type.lower() != property_type.lower():
            continue
        if max_price and prop.price > max_price:
            continue
        if location and location.lower() not in prop.location.lower():
            continue
        
        properties.append({
            "id": prop.id,
            "title": prop.title,
            "type": prop.type,
            "price": prop.price,
            "location": prop.location,
            "surface": prop.surface,
            "rooms": prop.rooms,
            "bedrooms": prop.bedrooms,
            "agent_id": prop.agent_id,
            "available_for_visit": prop.available_for_visit
        })
    
    return properties

def search_properties_by_criteria(criteria: Dict) -> List[Dict]:
    """
    Recherche avancée de propriétés selon plusieurs critères.
    
    Args:
        criteria: Dictionnaire avec les critères de recherche
    
    Returns:
        Liste des propriétés correspondant aux critères
    """
    properties = []
    
    for prop_id, prop in PROPERTIES_DB.items():
        match = True
        
        # Type de propriété
        if criteria.get("type") and prop.type.lower() != criteria["type"].lower():
            match = False
        
        # Prix
        if criteria.get("min_price") and prop.price < criteria["min_price"]:
            match = False
        if criteria.get("max_price") and prop.price > criteria["max_price"]:
            match = False
        
        # Surface
        if criteria.get("min_surface") and prop.surface < criteria["min_surface"]:
            match = False
        if criteria.get("max_surface") and prop.surface > criteria["max_surface"]:
            match = False
        
        # Nombre de chambres
        if criteria.get("min_bedrooms") and prop.bedrooms < criteria["min_bedrooms"]:
            match = False
        
        # Localisation
        if criteria.get("location") and criteria["location"].lower() not in prop.location.lower():
            match = False
        
        # Agent
        if criteria.get("agent_id") and prop.agent_id != criteria["agent_id"]:
            match = False
        
        if match:
            properties.append({
                "id": prop.id,
                "title": prop.title,
                "type": prop.type,
                "price": prop.price,
                "location": prop.location,
                "surface": prop.surface,
                "rooms": prop.rooms,
                "bedrooms": prop.bedrooms,
                "agent_id": prop.agent_id,
                "available_for_visit": prop.available_for_visit
            })
    
    return properties

def get_properties_by_agent(agent_id: str) -> List[Dict]:
    """
    Récupère toutes les propriétés gérées par un agent.
    
    Args:
        agent_id: Identifiant de l'agent
    
    Returns:
        Liste des propriétés de l'agent
    """
    properties = []
    
    for prop_id, prop in PROPERTIES_DB.items():
        if prop.agent_id == agent_id:
            properties.append({
                "id": prop.id,
                "title": prop.title,
                "type": prop.type,
                "price": prop.price,
                "location": prop.location,
                "surface": prop.surface,
                "rooms": prop.rooms,
                "bedrooms": prop.bedrooms,
                "available_for_visit": prop.available_for_visit
            })
    
    return properties

def get_property_summary(property_id: str) -> str:
    """
    Génère un résumé formaté d'une propriété.
    
    Args:
        property_id: Identifiant de la propriété
    
    Returns:
        Résumé formaté de la propriété
    """
    if property_id not in PROPERTIES_DB:
        return f"Propriété {property_id} non trouvée"
    
    prop = PROPERTIES_DB[property_id]
    
    summary = f"**{prop.title}**\n"
    summary += f"📍 **Localisation**: {prop.location}\n"
    summary += f"💰 **Prix**: {prop.price:,} €\n"
    summary += f"📐 **Surface**: {prop.surface} m²\n"
    summary += f"🏠 **Type**: {prop.type}\n"
    summary += f"🛏️ **Chambres**: {prop.bedrooms}\n"
    summary += f"🚪 **Pièces**: {prop.rooms}\n"
    summary += f"👨‍💼 **Agent**: {prop.agent_id}\n"
    summary += f"📝 **Description**: {prop.description}\n"
    
    if prop.features:
        summary += f"✨ **Équipements**: {', '.join(prop.features)}\n"
    
    return summary

def suggest_properties_for_client(client_preferences: Dict) -> List[Dict]:
    """
    Suggère des propriétés basées sur les préférences client.
    
    Args:
        client_preferences: Préférences du client
    
    Returns:
        Liste des propriétés suggérées
    """
    property_type = client_preferences.get("property_type", "").lower()
    budget_range = client_preferences.get("budget_range", "").lower()
    location = client_preferences.get("location_preference", "").lower()
    
    # Définir les critères de recherche basés sur les préférences
    criteria = {}
    
    if property_type:
        criteria["type"] = property_type
    
    if budget_range:
        if "luxe" in budget_range or "premium" in budget_range:
            criteria["min_price"] = 2000000
        elif "moyen" in budget_range:
            criteria["min_price"] = 500000
            criteria["max_price"] = 2000000
        elif "accessible" in budget_range or "économique" in budget_range:
            criteria["max_price"] = 500000
    
    if location:
        criteria["location"] = location
    
    return search_properties_by_criteria(criteria)
