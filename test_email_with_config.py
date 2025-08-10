#!/usr/bin/env python3
"""
Script de test avec configuration email factice
"""
import asyncio
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Configuration email factice pour le test
os.environ.update({
    'MAIL_USERNAME': 'test@example.com',
    'MAIL_PASSWORD': 'test_password',
    'MAIL_FROM': 'test@example.com',
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': '587',
    'MAIL_STARTTLS': 'true',
    'MAIL_SSL_TLS': 'false'
})

async def test_email_service():
    """Test du service email directement"""
    try:
        from src.core.email import email_service
        
        print("🧪 Test du service email...")
        
        # Données de test
        appointment_data = {
            "title": "Visite appartement T3",
            "start_iso": "2025-01-15T14:00:00+01:00",
            "end_iso": "2025-01-15T14:45:00+01:00",
            "location": "123 Rue de la Paix, Paris",
            "description": "Visite d'un appartement T3 avec balcon"
        }
        
        # Test d'envoi d'email
        success = await email_service.send_appointment_confirmation(
            client_email="client@example.com",
            client_name="Jean Dupont",
            appointment_data=appointment_data,
            agent_name="Marie Martin"
        )
        
        if success:
            print("✅ Service email fonctionne!")
        else:
            print("❌ Service email a échoué (normal sans vraie config SMTP)")
            
    except Exception as e:
        print(f"❌ Erreur service email: {e}")

async def test_create_event():
    """Test de création d'événement avec email"""
    try:
        from tools.create_event import create_event
        
        print("\n📅 Test de création d'événement...")
        
        start_time = datetime.now(ZoneInfo("Europe/Paris")) + timedelta(hours=1)
        end_time = start_time + timedelta(minutes=45)
        
        result = await create_event(
            agent_id="AGENT_TEST",
            start=start_time,
            end=end_time,
            title="Test de confirmation email",
            attendees=[
                {"email": "test@example.com", "name": "Client Test"}
            ],
            location="123 Rue de Test, Ville Test",
            description="Ceci est un test d'envoi d'email de confirmation.",
            send_email=True
        )
        
        print("✅ Événement créé avec succès!")
        print(f"   ID: {result['event_id']}")
        print(f"   Email envoyé: {result.get('email_sent', False)}")
        
        # Afficher le contenu HTML généré
        from src.core.email import email_service
        appointment_data = {
            "title": result.get('title', 'Test'),
            "start_iso": result['start_iso'],
            "end_iso": result['end_iso'],
            "location": "123 Rue de Test, Ville Test",
            "description": "Ceci est un test d'envoi d'email de confirmation."
        }
        
        html_content = email_service._create_confirmation_html(
            client_name="Client Test",
            appointment_data=appointment_data,
            start_dt=start_time,
            end_dt=end_time,
            agent_name="Agent Test"
        )
        
        print("\n📧 Aperçu de l'email HTML généré:")
        print("=" * 50)
        print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Erreur création événement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Test de la fonctionnalité d'envoi d'emails avec config factice")
    print("=" * 70)
    
    # Test du service email
    asyncio.run(test_email_service())
    
    # Test de création d'événement
    asyncio.run(test_create_event())
    
    print("\n✅ Tests terminés!")
    print("\n💡 Pour tester avec de vraies emails, configurez vos variables d'environnement:")
    print("   MAIL_USERNAME=your_email@gmail.com")
    print("   MAIL_PASSWORD=your_app_password")
    print("   MAIL_FROM=your_email@gmail.com")
