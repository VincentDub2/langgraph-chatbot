#!/usr/bin/env python3
"""
Script de démarrage pour la version refactorisée
"""
import argparse
import sys
import os
from pathlib import Path


def start_api():
    """Démarre l'API FastAPI"""
    print("🚀 Démarrage de l'API FastAPI...")
    os.system("python main.py")


def start_cli():
    """Démarre l'interface CLI"""
    print("💻 Démarrage de l'interface CLI...")
    os.system("python cli.py")


def start_gradio():
    """Démarre l'interface Gradio"""
    print("🎨 Démarrage de l'interface Gradio...")
    os.system("python gradio_app.py")


def run_tests():
    """Lance les tests"""
    print("🧪 Lancement des tests...")
    os.system("python -m pytest")


def show_help():
    """Affiche l'aide"""
    print("""
🤖 Chatbot Agent Immobilier - Version Refactorisée

Usage:
  python start_refactored.py [COMMANDE]

Commandes disponibles:
  api     - Démarre l'API FastAPI
  cli     - Démarre l'interface en ligne de commande
  gradio  - Démarre l'interface Gradio
  test    - Lance les tests
  help    - Affiche cette aide

Exemples:
  python start_refactored.py api
  python start_refactored.py cli
  python start_refactored.py gradio
  python start_refactored.py test
""")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Démarrage du chatbot refactorisé")
    parser.add_argument("command", nargs="?", default="help", 
                       choices=["api", "cli", "gradio", "test", "help"],
                       help="Commande à exécuter")
    
    args = parser.parse_args()
    
    if args.command == "api":
        start_api()
    elif args.command == "cli":
        start_cli()
    elif args.command == "gradio":
        start_gradio()
    elif args.command == "test":
        run_tests()
    else:
        show_help()


if __name__ == "__main__":
    main()
