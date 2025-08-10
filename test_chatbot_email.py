#!/usr/bin/env python3
"""
Test du chatbot avec fonctionnalité d'envoi d'email
"""
import asyncio
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


async def test_chatbot_appointment_creation():
    """Test de création de rendez-vous via le chatbot"""
    try:
        # Import du chatbot
        from src.graph.builder import create_graph
        
        print("🤖 Test du chatbot avec création de rendez-vous...")
        
        # Créer le graph du chatbot
        graph = create_graph()
        
        # Message de test pour créer un rendez-vous
        test_message = """
        Bonjour, je m'appelle Jean Dupont et mon email est vincentdubuc2@gmail.com.
        Je voudrais prendre un rendez-vous pour visiter un appartement T3 à Paris.
        Je suis disponible demain après-midi entre 14h et 16h.
        """
        
        # Configuration du thread
        config = {
            "configurable": {
                "thread_id": "test_thread_email",
                "user_id": "test_user"
            }
        }
        
        # Exécuter le chatbot
        print("📝 Envoi du message au chatbot...")
        result = await graph.ainvoke(
            {"messages": [{"role": "user", "content": test_message}]},
            config=config
        )
        
        print("✅ Réponse du chatbot reçue!")
        print(f"📊 Nombre de messages: {len(result['messages'])}")
        
        # Afficher la dernière réponse
        if result['messages']:
            last_message = result['messages'][-1]
            print(f"🤖 Réponse du chatbot:")
            print(f"   {last_message['content'][:200]}...")
        
        # Vérifier si un rendez-vous a été créé
        print("\n🔍 Vérification de la création de rendez-vous...")
        
        # Import des outils pour vérifier
        from tools.create_event import _EVENTS
        
        if _EVENTS:
            print(f"✅ {len(_EVENTS)} événement(s) créé(s)!")
            for event_id, event in _EVENTS.items():
                print(f"   📅 Événement: {event['title']}")
                print(f"   👥 Participants: {len(event['attendees'])}")
                print(f"   📧 Emails: {[a.get('email') for a in event['attendees'] if a.get('email')]}")
        else:
            print("❌ Aucun événement créé")
            
    except Exception as e:
        print(f"❌ Erreur lors du test du chatbot: {e}")
        import traceback
        traceback.print_exc()

async def test_direct_appointment_creation():
    """Test direct de création de rendez-vous avec email"""
    try:
        from tools.create_event import create_event
        
        print("\n📅 Test direct de création de rendez-vous...")
        
        # Créer un rendez-vous de test
        start_time = datetime.now(ZoneInfo("Europe/Paris")) + timedelta(days=1, hours=14)
        end_time = start_time + timedelta(minutes=45)
        
        result = await create_event(
            agent_id="AGENT_1",
            start=start_time,
            end=end_time,
            title="Visite appartement T3 - Test Chatbot",
            attendees=[
                {"email": "vincentdubuc2@gmail.com", "name": "Jean Dupont"}
            ],
            location="123 Rue de la Paix, Paris",
            description="Visite d'un appartement T3 avec balcon, 2ème étage",
            send_email=True
        )
        
        print("✅ Rendez-vous créé avec succès!")
        print(f"   🆔 ID: {result['event_id']}")
        print(f"   📧 Email envoyé: {result.get('email_sent', False)}")
        print(f"   📅 Date: {result['start_iso']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur création rendez-vous: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Test du chatbot avec fonctionnalité d'envoi d'email")
    print("=" * 60)
    
    # Test direct de création de rendez-vous
    asyncio.run(test_direct_appointment_creation())
    
    # Test du chatbot complet
    asyncio.run(test_chatbot_appointment_creation())
    
    print("\n✅ Tests terminés!")
    print("\n💡 Pour tester avec de vraies emails:")
    print("   1. Configurez vos variables d'environnement email")
    print("   2. Remplacez les emails de test par de vrais emails")
    print("   3. Relancez les tests")
