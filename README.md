# Chatbot Agent Immobilier - LangGraph

Un chatbot intelligent pour la gestion des rendez-vous immobiliers, développé avec LangGraph et LangChain.

## 🏠 Fonctionnalités

### Gestion des Rendez-vous
- ✅ Vérification des disponibilités des agents
- ✅ Réservation de créneaux de visite
- ✅ Génération de fichiers ICS pour les confirmations
- ✅ **Envoi automatique d'emails de confirmation aux clients**
- ✅ Gestion des conflits de planning

### Gestion des Agents
- ✅ Base de données des agents avec spécialités
- ✅ Recherche d'agents par spécialité
- ✅ Informations détaillées sur les agents
- ✅ Horaires de travail et disponibilités

### Gestion des Propriétés
- ✅ Base de données de propriétés immobilières
- ✅ Recherche avancée par critères
- ✅ Suggestions de biens selon les préférences client
- ✅ Informations détaillées sur les propriétés

### Validation et Gestion Client
- ✅ Validation des données client (email, téléphone, etc.)
- ✅ Suggestion d'agents selon les préférences
- ✅ Formatage des informations client

### API REST Complète
- ✅ Endpoints pour tous les services
- ✅ Support du streaming pour le chat
- ✅ Documentation automatique (Swagger/ReDoc)
- ✅ Gestion des threads de conversation

## 🛠️ Architecture

### Outils Disponibles

#### Gestion des Rendez-vous
- `check_availability(agent_id, window)` - Vérifier les créneaux disponibles
- `create_event(agent_id, start, end, title, ...)` - Créer un rendez-vous

#### Gestion des Agents
- `list_agents()` - Lister tous les agents
- `get_agent_info(agent_id)` - Informations d'un agent
- `find_agent_by_speciality(speciality)` - Recherche par spécialité
- `get_agent_availability_summary(agent_id)` - Résumé des horaires

#### Gestion des Propriétés
- `list_properties(type, max_price, location)` - Lister les propriétés
- `get_property_info(property_id)` - Informations d'une propriété
- `get_property_summary(property_id)` - Résumé formaté
- `search_properties_by_criteria(criteria)` - Recherche avancée
- `get_properties_by_agent(agent_id)` - Propriétés d'un agent
- `suggest_properties_for_client(preferences)` - Suggestions personnalisées

#### Validation Client
- `validate_client_data(client_data)` - Validation des données
- `suggest_agent_by_preferences(client_data)` - Suggestion d'agent

#### Utilitaires
- `calc(expression)` - Calculs mathématiques
- `now()` - Heure actuelle

## 🚀 Installation et Déploiement

### Option 1: Déploiement Docker (Recommandé)

#### Prérequis
- Docker et Docker Compose installés
- Variables d'environnement configurées

#### Démarrage rapide
```bash
# Cloner le projet
git clone <repository-url>
cd langgraph-chatbot

# Configurer les variables d'environnement
export API_KEY="votre_clé_api"
export BASE_URL="votre_url_base"

# Configuration email (optionnel, pour les confirmations automatiques)
export MAIL_USERNAME="votre_email@gmail.com"
export MAIL_PASSWORD="votre_mot_de_passe_application"
export MAIL_FROM="votre_email@gmail.com"

# Démarrer avec Docker
./start.sh dev
```

#### Commandes Docker disponibles
```bash
# Mode développement (avec logs en temps réel)
./start.sh dev

# Mode production (en arrière-plan)
./start.sh prod

# Exécuter les tests
./start.sh test

# Arrêter les services
./start.sh stop

# Voir les logs
./start.sh logs

# Nettoyer
./start.sh clean

# Afficher l'aide
./start.sh help
```

### Option 2: Développement Local avec UV

#### Prérequis
- Python 3.12+
- UV (installé automatiquement par le script)
- Variables d'environnement configurées

#### Démarrage local
```bash
# Configurer les variables d'environnement
export API_KEY="votre_clé_api"
export BASE_URL="votre_url_base"

# Démarrer en mode local
./start.sh local
```

#### Commandes UV disponibles
```bash
# Démarrer en mode développement local
./start.sh local

# Nettoyer l'environnement local
./start.sh clean-local

# Installation manuelle des dépendances
uv sync

# Exécuter l'API
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# Exécuter les tests
uv run python test_api.py
```

### Option 3: Installation Manuelle

#### Prérequis
- Python 3.12+
- UV installé
- Variables d'environnement configurées

#### Installation des dépendances
```bash
# Installer UV si nécessaire
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installer les dépendances
uv sync
```

#### Configuration des variables d'environnement
```bash
export API_KEY="votre_clé_api"
export BASE_URL="votre_url_base"
```

## 📊 Base de Données de Démonstration

### Agents Disponibles
- **agent1** : Marie Dubois - Spécialiste familial et investissement
- **agent2** : Pierre Martin - Expert commercial et bureaux  
- **agent3** : Sophie Bernard - Spécialiste luxe et international

### Propriétés Disponibles
- **prop1** : Appartement T3 - Quartier Latin (450k€)
- **prop2** : Maison familiale - Neuilly-sur-Seine (1.2M€)
- **prop3** : Bureau 200m² - La Défense (850k€)
- **prop4** : Local commercial - Champs-Élysées (2.5M€)
- **prop5** : Penthouse de luxe - 16ème arrondissement (3.5M€)
- **prop6** : Villa de prestige - Saint-Tropez (8.5M€)

## 🎯 Utilisation

### Interface Gradio
```bash
uv run python run_gradio.py
```

### Interface en ligne de commande
```bash
uv run python app.py
```

### Interface streaming
```bash
uv run python gradio_streaming.py
```

### API REST
```bash
# Démarrer l'API avec UV
./start.sh local

# Ou avec Docker
./start.sh dev

# Ou manuellement
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

## 🔌 API REST

### Endpoints Principaux

#### Chat
- `POST /chat` - Envoyer un message au chatbot
- `POST /chat/stream` - Chat en streaming

#### Agents
- `GET /agents` - Lister tous les agents
- `GET /agents/{agent_id}` - Informations d'un agent

#### Propriétés
- `GET /properties` - Lister les propriétés
- `GET /properties/{property_id}` - Informations d'une propriété
- `GET /search/properties` - Recherche avancée

#### Rendez-vous
- `POST /availability` - Vérifier les disponibilités
- `POST /appointments` - Créer un rendez-vous

#### Threads
- `GET /threads/{thread_id}` - Informations d'un thread
- `DELETE /threads/{thread_id}` - Supprimer un thread

#### Utilitaires
- `GET /health` - Vérification de l'état
- `GET /` - Point d'entrée

### Documentation API
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Exemples d'utilisation

#### Chat simple
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour, je cherche un appartement à Paris",
    "stream": false
  }'
```

#### Chat en streaming
```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Pouvez-vous me montrer les agents disponibles ?",
    "stream": true
  }'
```

#### Lister les agents
```bash
curl -X GET "http://localhost:8000/agents"
```

#### Rechercher des propriétés
```bash
curl -X GET "http://localhost:8000/search/properties?type=Appartement&max_price=500000&location=Paris"
```

#### Vérifier les disponibilités
```bash
curl -X POST "http://localhost:8000/availability" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent1",
    "window": "tomorrow"
  }'
```

## 🔄 Processus de Réservation

1. **Accueil** - Salutation et présentation
2. **Collecte d'informations** - Nom, email, préférences
3. **Validation** - Vérification des données client
4. **Recherche** - Suggestion d'agents et de propriétés
5. **Vérification disponibilités** - Consultation des créneaux
6. **Confirmation** - Création du rendez-vous et envoi d'email de confirmation

## 📧 Configuration Email

Le chatbot peut envoyer automatiquement des emails de confirmation de rendez-vous aux clients.

### Configuration requise

Ajoutez ces variables à votre fichier `.env` :

```bash
# Configuration Email
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
```

### Fournisseurs supportés

- **Gmail** : Utilisez un mot de passe d'application
- **Outlook/Hotmail** : Configuration standard
- **Serveurs SMTP personnalisés** : Configuration flexible

### Test de la configuration

```bash
# Test avec configuration factice
uv run python test_email_with_config.py

# Test avec vraie configuration
uv run python test_email.py
```

📖 **Documentation complète** : Consultez `EMAIL_SETUP.md` pour plus de détails.

## 📝 Exemples d'Utilisation

### Recherche de propriétés
```
Client: "Je cherche un appartement à Paris pour moins de 500k€"
Bot: Utilise list_properties(property_type="Appartement", max_price="500000", location="Paris")
```

### Vérification de disponibilités
```
Client: "Je voudrais un rendez-vous demain après-midi"
Bot: Utilise check_availability(agent_id="agent1", window="tomorrow afternoon")
```

### Création de rendez-vous
```
Bot: Utilise create_event(
    agent_id="agent1",
    start="2025-01-15T14:00:00",
    end="2025-01-15T15:00:00",
    title="Visite appartement T3",
    attendees='[{"name": "Jean Dupont", "email": "jean@example.com"}]',
    location="5ème arrondissement, Paris"
)
```

## 🧪 Tests

### Tests de l'API
```bash
# Exécuter les tests automatiquement
./start.sh test

# Ou manuellement avec UV
uv run python test_api.py

# Ou avec Python standard
python test_api.py
```

### Tests manuels
```bash
# Démarrer l'API
./start.sh local

# Dans un autre terminal, tester
curl http://localhost:8000/health
```

## 🎨 Personnalisation

### Ajout d'agents
Modifiez le fichier `tools/agent_info.py` pour ajouter de nouveaux agents.

### Ajout de propriétés
Modifiez le fichier `tools/property_manager.py` pour ajouter de nouvelles propriétés.

### Modification du prompt
Éditez le fichier `prompts/chatbot_v1.md` pour personnaliser le comportement du chatbot.

### Configuration Docker
Modifiez `docker-compose.yml` pour ajuster les paramètres de déploiement.

### Gestion des dépendances avec UV
```bash
# Ajouter une dépendance
uv add nom_package

# Ajouter une dépendance de développement
uv add --dev nom_package

# Mettre à jour les dépendances
uv sync

# Générer requirements.txt
uv pip compile pyproject.toml -o requirements.txt
```

## 🔧 Configuration Avancée

### Horaires de travail
Les horaires sont configurés dans `tools/agent_info.py` :
- Lundi-Vendredi : 9h-12h et 14h-18h
- Samedi : Variable selon l'agent
- Dimanche : Fermé

### Validation des données
Les règles de validation sont dans `tools/client_validation.py` :
- Email : Format standard
- Téléphone : Format français (+33 ou 0)
- Nom : 2-50 caractères alphabétiques

### Variables d'environnement
```bash
# Obligatoires
API_KEY=votre_clé_api
BASE_URL=votre_url_base

# Optionnelles
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### Configuration UV
Le projet utilise UV pour la gestion des dépendances avec :
- `pyproject.toml` : Configuration du projet et dépendances
- `uv.lock` : Verrouillage des versions
- Environnement virtuel automatique dans `.venv/`

## 🐛 Dépannage

### Erreurs courantes
1. **Fichier de prompt non trouvé** : Vérifiez que `prompts/chatbot_v1.md` existe
2. **Variables d'environnement manquantes** : Configurez API_KEY et BASE_URL
3. **Erreurs de validation** : Vérifiez le format des données client
4. **Port déjà utilisé** : Changez le port dans docker-compose.yml
5. **UV non installé** : Le script l'installe automatiquement

### Logs
```bash
# Voir les logs Docker
./start.sh logs

# Ou directement
docker-compose logs -f chatbot-api

# Logs de l'API locale
uv run uvicorn api:app --log-level debug
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Nettoyage
```bash
# Nettoyer Docker
./start.sh clean

# Nettoyer l'environnement local
./start.sh clean-local
```

## 📈 Améliorations Futures

- [ ] Intégration avec un vrai CRM
- [ ] Notifications par email/SMS
- [ ] Interface web complète
- [ ] Gestion des paiements
- [ ] Analytics et reporting
- [ ] Support multilingue avancé
- [ ] Base de données persistante
- [ ] Authentification et autorisation
- [ ] Rate limiting
- [ ] Monitoring et alertes

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

---

**Développé avec ❤️ pour les agences immobilières**
