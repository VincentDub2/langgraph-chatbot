#!/usr/bin/env python3
"""
Script de test pour l'API Chatbot Immobilier
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "health": "/health",
    "root": "/",
    "chat": "/chat",
    "chat_stream": "/chat/stream",
    "agents": "/agents",
    "properties": "/properties",
    "availability": "/availability",
    "appointments": "/appointments",
    "search": "/search/properties"
}

def test_health_check():
    """Test du health check"""
    print("🔍 Test du health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data}")
            return True
        else:
            print(f"❌ Health check échoué: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du health check: {e}")
        return False

def test_root():
    """Test du point d'entrée"""
    print("\n🔍 Test du point d'entrée...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Point d'entrée OK: {data}")
            return True
        else:
            print(f"❌ Point d'entrée échoué: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test du point d'entrée: {e}")
        return False

def test_chat():
    """Test du chat"""
    print("\n🔍 Test du chat...")
    try:
        payload = {
            "message": "Bonjour, je cherche un appartement à Paris",
            "stream": False
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat OK: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat échoué: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test du chat: {e}")
        return False

def test_chat_stream():
    """Test du chat en streaming"""
    print("\n🔍 Test du chat en streaming...")
    try:
        payload = {
            "message": "Pouvez-vous me montrer les agents disponibles ?",
            "stream": True
        }
        response = requests.post(f"{BASE_URL}/chat/stream", json=payload, stream=True)
        if response.status_code == 200:
            print("✅ Streaming OK:")
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Enlever 'data: '
                        try:
                            data = json.loads(data_str)
                            if 'chunk' in data:
                                print(f"   📝 Chunk: {data['chunk']}", end='')
                            elif 'done' in data:
                                print(f"\n   ✅ Streaming terminé")
                                break
                            elif 'error' in data:
                                print(f"\n   ❌ Erreur: {data['error']}")
                                return False
                        except json.JSONDecodeError:
                            continue
            return True
        else:
            print(f"❌ Streaming échoué: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test du streaming: {e}")
        return False

def test_agents():
    """Test des agents"""
    print("\n🔍 Test des agents...")
    try:
        # Lister tous les agents
        response = requests.get(f"{BASE_URL}/agents")
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ Agents listés: {len(agents)} agents trouvés")
            
            # Test d'un agent spécifique
            if agents:
                agent_id = agents[0]['id']
                response = requests.get(f"{BASE_URL}/agents/{agent_id}")
                if response.status_code == 200:
                    agent = response.json()
                    print(f"✅ Agent {agent_id} récupéré: {agent['name']}")
                    return True
                else:
                    print(f"❌ Erreur lors de la récupération de l'agent {agent_id}")
                    return False
            return True
        else:
            print(f"❌ Liste des agents échouée: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test des agents: {e}")
        return False

def test_properties():
    """Test des propriétés"""
    print("\n🔍 Test des propriétés...")
    try:
        # Lister toutes les propriétés
        response = requests.get(f"{BASE_URL}/properties")
        if response.status_code == 200:
            properties = response.json()
            print(f"✅ Propriétés listées: {len(properties)} propriétés trouvées")
            
            # Test d'une propriété spécifique
            if properties:
                property_id = properties[0]['id']
                response = requests.get(f"{BASE_URL}/properties/{property_id}")
                if response.status_code == 200:
                    property_info = response.json()
                    print(f"✅ Propriété {property_id} récupérée: {property_info['title']}")
                    return True
                else:
                    print(f"❌ Erreur lors de la récupération de la propriété {property_id}")
                    return False
            return True
        else:
            print(f"❌ Liste des propriétés échouée: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test des propriétés: {e}")
        return False

def test_availability():
    """Test des disponibilités"""
    print("\n🔍 Test des disponibilités...")
    try:
        payload = {
            "agent_id": "agent1",
            "window": "tomorrow"
        }
        response = requests.post(f"{BASE_URL}/availability", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Disponibilités récupérées pour {data['agent_id']}")
            return True
        else:
            print(f"❌ Disponibilités échouées: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test des disponibilités: {e}")
        return False

def test_search():
    """Test de la recherche"""
    print("\n🔍 Test de la recherche...")
    try:
        params = {
            "type": "Appartement",
            "max_price": 500000,
            "location": "Paris"
        }
        response = requests.get(f"{BASE_URL}/search/properties", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recherche OK: {data['count']} propriétés trouvées")
            return True
        else:
            print(f"❌ Recherche échouée: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de la recherche: {e}")
        return False

def test_appointment():
    """Test de création de rendez-vous"""
    print("\n🔍 Test de création de rendez-vous...")
    try:
        from datetime import datetime, timedelta
        
        # Créer un rendez-vous pour demain
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0).isoformat()
        end_time = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0).isoformat()
        
        payload = {
            "agent_id": "agent1",
            "start": start_time,
            "end": end_time,
            "title": "Visite appartement T3",
            "attendees": [
                {"name": "Jean Dupont", "email": "jean@example.com"}
            ],
            "location": "5ème arrondissement, Paris",
            "description": "Visite d'un appartement T3 dans le Quartier Latin"
        }
        
        response = requests.post(f"{BASE_URL}/appointments", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Rendez-vous créé: {data['message']}")
            return True
        else:
            print(f"❌ Création de rendez-vous échouée: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de création de rendez-vous: {e}")
        return False

def run_all_tests():
    """Exécuter tous les tests"""
    print("🚀 Démarrage des tests de l'API Chatbot Immobilier")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root),
        ("Chat", test_chat),
        ("Chat Streaming", test_chat_stream),
        ("Agents", test_agents),
        ("Properties", test_properties),
        ("Availability", test_availability),
        ("Search", test_search),
        ("Appointment", test_appointment)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'API fonctionne correctement.")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez la configuration de l'API.")
    
    return passed == total

if __name__ == "__main__":
    # Attendre que l'API soit prête
    print("⏳ Attente du démarrage de l'API...")
    time.sleep(5)
    
    success = run_all_tests()
    exit(0 if success else 1)
