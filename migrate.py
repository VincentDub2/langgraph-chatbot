#!/usr/bin/env python3
"""
Script de migration pour la refactorisation du projet
"""
import os
import shutil
import sys
from pathlib import Path


def backup_old_files():
    """Sauvegarde les anciens fichiers"""
    backup_dir = Path("backup_old")
    backup_dir.mkdir(exist_ok=True)
    
    old_files = [
        "api.py",
        "graph.py", 
        "prompt_manager.py",
        "app.py"
    ]
    
    print("📦 Sauvegarde des anciens fichiers...")
    for file in old_files:
        if Path(file).exists():
            shutil.copy2(file, backup_dir / file)
            print(f"  ✓ {file} sauvegardé")
        else:
            print(f"  ⚠ {file} non trouvé")


def create_directories():
    """Crée les nouveaux répertoires"""
    directories = [
        "src",
        "src/core",
        "src/graph", 
        "src/api",
        "src/api/routes",
        "src/cli",
        "src/ui"
    ]
    
    print("📁 Création des répertoires...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}/")


def check_imports():
    """Vérifie que les imports fonctionnent"""
    print("🔍 Vérification des imports...")
    
    try:
        # Test des imports principaux
        import src.core.config
        import src.core.models
        import src.core.prompts
        import src.graph.tools
        import src.graph.builder
        import src.api.app
        print("  ✓ Tous les imports fonctionnent")
        return True
    except ImportError as e:
        print(f"  ❌ Erreur d'import: {e}")
        return False


def test_endpoints():
    """Teste les points d'entrée"""
    print("🧪 Test des points d'entrée...")
    
    entry_points = [
        "main.py",
        "cli.py", 
        "gradio_app.py"
    ]
    
    for entry_point in entry_points:
        if Path(entry_point).exists():
            print(f"  ✓ {entry_point} existe")
        else:
            print(f"  ❌ {entry_point} manquant")


def main():
    """Fonction principale de migration"""
    print("🚀 Migration du projet Chatbot Immobilier")
    print("=" * 50)
    
    # Étape 1: Sauvegarde
    backup_old_files()
    
    # Étape 2: Création des répertoires
    create_directories()
    
    # Étape 3: Vérification des imports
    if not check_imports():
        print("❌ Migration échouée: problèmes d'imports")
        sys.exit(1)
    
    # Étape 4: Test des points d'entrée
    test_endpoints()
    
    print("\n✅ Migration terminée avec succès!")
    print("\n📋 Prochaines étapes:")
    print("1. Testez l'application: python main.py")
    print("2. Vérifiez que tout fonctionne correctement")
    print("3. Supprimez les anciens fichiers si tout est OK")
    print("4. Consultez README_REFACTOR.md pour plus d'informations")


if __name__ == "__main__":
    main()
