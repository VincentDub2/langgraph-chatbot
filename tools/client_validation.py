from __future__ import annotations
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json

@dataclass
class ClientInfo:
    name: str
    email: str
    phone: Optional[str] = None
    preferred_agent: Optional[str] = None
    property_type: Optional[str] = None
    budget_range: Optional[str] = None
    location_preference: Optional[str] = None
    notes: Optional[str] = None

class ClientValidationError(Exception):
    """Exception levée lors de la validation des données client."""
    pass

# Patterns de validation
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_PATTERN = re.compile(r'^(\+33|0)[1-9](\d{8})$')
NAME_PATTERN = re.compile(r'^[a-zA-ZÀ-ÿ\s-]{2,50}$')

def validate_email(email: str) -> bool:
    """
    Valide le format d'un email.
    
    Args:
        email: Adresse email à valider
    
    Returns:
        True si l'email est valide, False sinon
    """
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_PATTERN.match(email.strip()))

def validate_phone(phone: str) -> bool:
    """
    Valide le format d'un numéro de téléphone français.
    
    Args:
        phone: Numéro de téléphone à valider
    
    Returns:
        True si le numéro est valide, False sinon
    """
    if not phone:
        return True  # Le téléphone est optionnel
    
    if not isinstance(phone, str):
        return False
    
    # Nettoie le numéro
    clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone.strip())
    return bool(PHONE_PATTERN.match(clean_phone))

def validate_name(name: str) -> bool:
    """
    Valide le format d'un nom.
    
    Args:
        name: Nom à valider
    
    Returns:
        True si le nom est valide, False sinon
    """
    if not name or not isinstance(name, str):
        return False
    return bool(NAME_PATTERN.match(name.strip()))

def format_phone(phone: str) -> str:
    """
    Formate un numéro de téléphone français.
    
    Args:
        phone: Numéro de téléphone à formater
    
    Returns:
        Numéro formaté
    """
    if not phone:
        return ""
    
    # Nettoie le numéro
    clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone.strip())
    
    # Ajoute le préfixe +33 si nécessaire
    if clean_phone.startswith('0'):
        clean_phone = '+33' + clean_phone[1:]
    elif not clean_phone.startswith('+33'):
        clean_phone = '+33' + clean_phone
    
    return clean_phone

def validate_client_data(client_data: Dict) -> Tuple[bool, List[str]]:
    """
    Valide toutes les données client.
    
    Args:
        client_data: Dictionnaire contenant les données client
    
    Returns:
        Tuple (is_valid, list_of_errors)
    """
    errors = []
    
    # Validation du nom
    name = client_data.get('name', '').strip()
    if not name:
        errors.append("Le nom est obligatoire")
    elif not validate_name(name):
        errors.append("Le nom doit contenir entre 2 et 50 caractères alphabétiques")
    
    # Validation de l'email
    email = client_data.get('email', '').strip()
    if not email:
        errors.append("L'email est obligatoire")
    elif not validate_email(email):
        errors.append("Format d'email invalide")
    
    # Validation du téléphone (optionnel)
    phone = client_data.get('phone', '').strip()
    if phone and not validate_phone(phone):
        errors.append("Format de numéro de téléphone invalide")
    
    # Validation de l'agent préféré
    preferred_agent = client_data.get('preferred_agent')
    if preferred_agent and preferred_agent not in ['agent1', 'agent2', 'agent3']:
        errors.append("Agent invalide. Agents disponibles: agent1, agent2, agent3")
    
    return len(errors) == 0, errors

def create_client_info(client_data: Dict) -> ClientInfo:
    """
    Crée un objet ClientInfo à partir des données validées.
    
    Args:
        client_data: Dictionnaire contenant les données client
    
    Returns:
        Objet ClientInfo
    
    Raises:
        ClientValidationError: Si les données sont invalides
    """
    is_valid, errors = validate_client_data(client_data)
    if not is_valid:
        raise ClientValidationError(f"Données client invalides: {'; '.join(errors)}")
    
    return ClientInfo(
        name=client_data.get('name', '').strip(),
        email=client_data.get('email', '').strip().lower(),
        phone=format_phone(client_data.get('phone', '')) if client_data.get('phone') else None,
        preferred_agent=client_data.get('preferred_agent'),
        property_type=client_data.get('property_type'),
        budget_range=client_data.get('budget_range'),
        location_preference=client_data.get('location_preference'),
        notes=client_data.get('notes')
    )

def suggest_agent_by_preferences(client_data: Dict) -> Optional[str]:
    """
    Suggère un agent basé sur les préférences du client.
    
    Args:
        client_data: Données client avec préférences
    
    Returns:
        ID de l'agent suggéré ou None
    """
    property_type = client_data.get('property_type', '').lower()
    budget_range = client_data.get('budget_range', '').lower()
    
    # Logique de suggestion basée sur les spécialités
    if any(word in property_type for word in ['appartement', 'maison', 'familial', 'investissement']):
        return 'agent1'  # Marie Dubois - spécialiste familial
    elif any(word in property_type for word in ['bureau', 'commercial', 'terrain', 'local']):
        return 'agent2'  # Pierre Martin - spécialiste commercial
    elif any(word in property_type for word in ['luxe', 'villa', 'penthouse', 'international']) or 'luxury' in budget_range:
        return 'agent3'  # Sophie Bernard - spécialiste luxe
    
    return None

def format_client_summary(client_info: ClientInfo) -> str:
    """
    Formate un résumé des informations client.
    
    Args:
        client_info: Informations client
    
    Returns:
        Résumé formaté
    """
    summary = f"**Client**: {client_info.name}\n"
    summary += f"**Email**: {client_info.email}\n"
    
    if client_info.phone:
        summary += f"**Téléphone**: {client_info.phone}\n"
    
    if client_info.property_type:
        summary += f"**Type de bien**: {client_info.property_type}\n"
    
    if client_info.budget_range:
        summary += f"**Budget**: {client_info.budget_range}\n"
    
    if client_info.location_preference:
        summary += f"**Localisation souhaitée**: {client_info.location_preference}\n"
    
    if client_info.preferred_agent:
        summary += f"**Agent préféré**: {client_info.preferred_agent}\n"
    
    if client_info.notes:
        summary += f"**Notes**: {client_info.notes}\n"
    
    return summary

def validate_appointment_data(appointment_data: Dict) -> Tuple[bool, List[str]]:
    """
    Valide les données de rendez-vous.
    
    Args:
        appointment_data: Données du rendez-vous
    
    Returns:
        Tuple (is_valid, list_of_errors)
    """
    errors = []
    
    # Validation de l'agent
    agent_id = appointment_data.get('agent_id')
    if not agent_id or agent_id not in ['agent1', 'agent2', 'agent3']:
        errors.append("Agent invalide ou manquant")
    
    # Validation des dates
    start_time = appointment_data.get('start_time')
    end_time = appointment_data.get('end_time')
    
    if not start_time or not end_time:
        errors.append("Date de début et de fin requises")
    
    # Validation du titre
    title = appointment_data.get('title', '').strip()
    if not title:
        errors.append("Titre du rendez-vous requis")
    
    return len(errors) == 0, errors
