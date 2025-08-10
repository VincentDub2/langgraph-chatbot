#!/usr/bin/env python3
"""
Script de test pour l'envoi d'emails de confirmation de rendez-vous
"""
import asyncio
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
_ = load_dotenv()

# Test de la création d'événement avec email
async def test_create_event_with_email():
    """Test de création d'événement avec envoi d'email"""
    try:
        from tools.create_event import create_event
        
        # Vérifier si la configuration email est présente
        required_vars = ['MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_FROM']
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print("⚠️  Variables d'environnement email manquantes:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\n📧 Pour configurer l'envoi d'emails, ajoutez ces variables à votre fichier .env:")
            print("   MAIL_USERNAME=your_email@gmail.com")
            print("   MAIL_PASSWORD=your_app_password")
            print("   MAIL_FROM=your_email@gmail.com")
            print("\n📖 Consultez EMAIL_SETUP.md pour plus de détails.")
            return
        
        print("✅ Configuration email détectée")
        
        # Créer un événement de test
        start_time = datetime.now(TZ) + timedelta(hours=1)
        end_time = start_time + timedelta(minutes=45)
        
        print(f"📅 Création d'un événement de test pour {start_time.strftime('%H:%M')}")
        
        result = await create_event(
            agent_id="AGENT_TEST",
            start=start_time,
            end=end_time,
            title="Test de confirmation email",
            attendees=[
                {"email": "vincentdubuc2@gmail.com", "name": "Client Test"}
            ],
            location="123 Rue de Test, Ville Test",
            description="Ceci est un test d'envoi d'email de confirmation.",
            send_email=True
        )
        
        print("✅ Événement créé avec succès!")
        print(f"   ID: {result['event_id']}")
        print(f"   Email envoyé: {result.get('email_sent', False)}")
        
        if result.get('email_sent'):
            print("📧 Email de confirmation envoyé avec succès!")
        else:
            print("❌ Échec de l'envoi de l'email")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

# Test de la version synchrone
def test_create_event_sync():
    """Test de la version synchrone"""
    try:
        from tools.create_event import create_event_sync
        
        print("\n🔄 Test de la version synchrone...")
        
        start_time = datetime.now(TZ) + timedelta(hours=2)
        end_time = start_time + timedelta(minutes=45)
        
        result = create_event_sync(
            agent_id="AGENT_SYNC",
            start=start_time,
            end=end_time,
            title="Test synchrone",
            attendees=[
                {"email": "sync@example.com", "name": "Client Sync"}
            ],
            location="456 Avenue Sync, Ville Sync",
            description="Test de la version synchrone.",
            send_email=True
        )
        
        print("✅ Version synchrone fonctionne!")
        print(f"   Email envoyé: {result.get('email_sent', False)}")
        
    except Exception as e:
        print(f"❌ Erreur version synchrone: {e}")

if __name__ == "__main__":
    TZ = ZoneInfo("Europe/Paris")
    
    print("🧪 Test de la fonctionnalité d'envoi d'emails")
    print("=" * 50)
    
    # Test asynchrone
    asyncio.run(test_create_event_with_email())
    
    # Test synchrone
    test_create_event_sync()
    
    print("\n✅ Tests terminés!")
