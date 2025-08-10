#!/bin/bash

# Script de démarrage pour le Chatbot Agent Immobilier
# Usage: ./start.sh [dev|prod|test]

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Chatbot Agent Immobilier${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Vérifier si Docker est installé
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    print_message "Docker et Docker Compose sont installés"
}

# Vérifier les variables d'environnement
check_env() {
    if [ -z "$API_KEY" ]; then
        print_warning "Variable API_KEY non définie. Utilisez: export API_KEY='votre_clé'"
    fi
    
    if [ -z "$BASE_URL" ]; then
        print_warning "Variable BASE_URL non définie. Utilisez: export BASE_URL='votre_url'"
    fi
}

# Créer les répertoires nécessaires
create_directories() {
    print_message "Création des répertoires nécessaires..."
    mkdir -p ics_out
    mkdir -p logs
    print_message "Répertoires créés"
}

# Vérifier si uv est installé localement
check_uv() {
    if command -v uv &> /dev/null; then
        print_message "UV est installé localement"
        return 0
    else
        print_warning "UV n'est pas installé localement. Installation automatique..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.cargo/env
        print_message "UV installé avec succès"
    fi
}

# Mode développement
start_dev() {
    print_message "Démarrage en mode développement..."
    
    # Construire l'image
    print_message "Construction de l'image Docker avec UV..."
    docker-compose build chatbot-api
    
    # Démarrer le service
    print_message "Démarrage du service..."
    docker-compose up chatbot-api
    
    print_message "API disponible sur http://localhost:8000"
    print_message "Documentation: http://localhost:8000/docs"
}

# Mode production
start_prod() {
    print_message "Démarrage en mode production..."
    
    # Vérifier les variables d'environnement
    if [ -z "$API_KEY" ] || [ -z "$BASE_URL" ]; then
        print_error "Les variables API_KEY et BASE_URL doivent être définies en production"
        exit 1
    fi
    
    # Construire et démarrer tous les services
    print_message "Construction des images..."
    docker-compose --profile production build
    
    print_message "Démarrage des services..."
    docker-compose --profile production up -d
    
    print_message "Services démarrés en arrière-plan"
    print_message "API disponible sur http://localhost:8000"
    print_message "Nginx disponible sur http://localhost:80"
}

# Mode test
start_test() {
    print_message "Démarrage en mode test..."
    
    # Démarrer le service en arrière-plan
    docker-compose up -d chatbot-api
    
    # Attendre que l'API soit prête
    print_message "Attente du démarrage de l'API..."
    sleep 10
    
    # Exécuter les tests
    print_message "Exécution des tests..."
    python test_api.py
    
    # Arrêter le service
    print_message "Arrêt du service..."
    docker-compose down
    
    print_message "Tests terminés"
}

# Mode développement local (sans Docker)
start_local() {
    print_message "Démarrage en mode développement local..."
    
    # Vérifier uv
    check_uv
    
    # Installer les dépendances
    print_message "Installation des dépendances avec UV..."
    uv sync
    
    # Démarrer l'API
    print_message "Démarrage de l'API..."
    uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
    
    print_message "API disponible sur http://localhost:8000"
    print_message "Documentation: http://localhost:8000/docs"
}

# Arrêter les services
stop_services() {
    print_message "Arrêt des services..."
    docker-compose down
    print_message "Services arrêtés"
}

# Afficher les logs
show_logs() {
    print_message "Affichage des logs..."
    docker-compose logs -f chatbot-api
}

# Nettoyer
cleanup() {
    print_message "Nettoyage des conteneurs et images..."
    docker-compose down --rmi all --volumes --remove-orphans
    print_message "Nettoyage terminé"
}

# Nettoyer l'environnement local
cleanup_local() {
    print_message "Nettoyage de l'environnement local..."
    if [ -d ".venv" ]; then
        rm -rf .venv
        print_message "Environnement virtuel supprimé"
    fi
    print_message "Nettoyage terminé"
}

# Afficher l'aide
show_help() {
    echo "Usage: $0 [COMMANDE]"
    echo ""
    echo "Commandes disponibles:"
    echo "  dev     - Démarrer en mode développement (Docker)"
    echo "  local   - Démarrer en mode développement local (UV)"
    echo "  prod    - Démarrer en mode production (Docker)"
    echo "  test    - Exécuter les tests"
    echo "  stop    - Arrêter les services"
    echo "  logs    - Afficher les logs"
    echo "  clean   - Nettoyer les conteneurs et images"
    echo "  clean-local - Nettoyer l'environnement local"
    echo "  help    - Afficher cette aide"
    echo ""
    echo "Variables d'environnement:"
    echo "  API_KEY   - Clé API pour le modèle de langage"
    echo "  BASE_URL  - URL de base pour l'API"
    echo ""
    echo "Exemples:"
    echo "  export API_KEY='votre_clé'"
    echo "  export BASE_URL='votre_url'"
    echo "  $0 dev"
    echo "  $0 local"
}

# Script principal
main() {
    print_header
    
    # Vérifications préalables
    check_docker
    check_env
    create_directories
    
    # Traitement des commandes
    case "${1:-dev}" in
        "dev")
            start_dev
            ;;
        "local")
            start_local
            ;;
        "prod")
            start_prod
            ;;
        "test")
            start_test
            ;;
        "stop")
            stop_services
            ;;
        "logs")
            show_logs
            ;;
        "clean")
            cleanup
            ;;
        "clean-local")
            cleanup_local
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Commande inconnue: $1"
            show_help
            exit 1
            ;;
    esac
}

# Exécuter le script principal
main "$@"
