#!/usr/bin/env python3
"""
Script de nettoyage après la refactorisation
"""
import os
import shutil
from pathlib import Path


def cleanup_old_files():
    """Supprime les anciens fichiers après vérification"""
    old_files = [
        "api.py",
        "graph.py", 
        "prompt_manager.py",
        "app.py"
    ]
    
    print("🧹 Nettoyage des anciens fichiers...")
    for file in old_files:
        if Path(file).exists():
            print(f"  ❓ Supprimer {file} ? (y/N): ", end="")
            response = input().strip().lower()
            if response == 'y':
                os.remove(file)
                print(f"  ✓ {file} supprimé")
            else:
                print(f"  ⏭ {file} conservé")
        else:
            print(f"  ⚠ {file} n'existe pas")


def cleanup_backup():
    """Supprime le dossier de sauvegarde"""
    backup_dir = Path("backup_old")
    if backup_dir.exists():
        print(f"  ❓ Supprimer le dossier de sauvegarde {backup_dir} ? (y/N): ", end="")
        response = input().strip().lower()
        if response == 'y':
            shutil.rmtree(backup_dir)
            print(f"  ✓ {backup_dir} supprimé")
        else:
            print(f"  ⏭ {backup_dir} conservé")


def main():
    """Fonction principale de nettoyage"""
    print("🧹 Nettoyage après refactorisation")
    print("=" * 40)
    
    cleanup_old_files()
    cleanup_backup()
    
    print("\n✅ Nettoyage terminé!")
    print("\n🎉 Votre projet est maintenant entièrement refactorisé!")
    print("📖 Consultez README_REFACTOR.md pour plus d'informations")


if __name__ == "__main__":
    main()
