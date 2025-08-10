#!/usr/bin/env python3
"""
Script simple pour lancer l'interface Gradio du chatbot
"""

from gradio_app import create_interface

if __name__ == "__main__":
    print("🚀 Lancement de l'interface Gradio...")
    print("📱 L'interface sera disponible à l'adresse: http://localhost:7860")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print("-" * 50)
    
    interface = create_interface()
    interface.launch(
        server_port=7860,
        show_error=True,
        debug=True
    )
