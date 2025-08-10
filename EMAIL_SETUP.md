# Configuration Email pour les Confirmations de Rendez-vous

Ce document explique comment configurer l'envoi automatique d'emails de confirmation de rendez-vous.

## Variables d'environnement requises

Ajoutez ces variables à votre fichier `.env` :

```bash
# Configuration Email
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password_here
MAIL_FROM=your_email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
```

## Configuration par fournisseur d'email

### Gmail
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
```

**Important** : Pour Gmail, vous devez utiliser un "mot de passe d'application" et non votre mot de passe principal.

### Outlook/Hotmail
```bash
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
```

### Serveur SMTP personnalisé
```bash
MAIL_SERVER=your_smtp_server.com
MAIL_PORT=587
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
```

## Comment obtenir un mot de passe d'application Gmail

1. Allez sur [myaccount.google.com](https://myaccount.google.com)
2. Cliquez sur "Sécurité"
3. Activez la "Validation en 2 étapes" si ce n'est pas déjà fait
4. Cliquez sur "Mots de passe d'application"
5. Sélectionnez "Autre (nom personnalisé)" et donnez un nom (ex: "Chatbot")
6. Copiez le mot de passe généré et utilisez-le dans `MAIL_PASSWORD`

## Test de la configuration

Pour tester que votre configuration email fonctionne, vous pouvez exécuter :

```bash
python tools/create_event.py
```

Cela créera un événement de test et tentera d'envoyer un email de confirmation.

## Fonctionnalités

- ✅ Envoi automatique d'email de confirmation lors de la création d'un rendez-vous
- ✅ Email HTML avec mise en forme professionnelle
- ✅ Email texte en fallback
- ✅ Gestion des erreurs d'envoi
- ✅ Support de plusieurs participants par rendez-vous
- ✅ Compatibilité avec les fournisseurs d'email populaires

## Format de l'email

L'email de confirmation contient :
- Nom et email du client
- Détails du rendez-vous (date, heure, lieu, agent)
- Description du rendez-vous
- Instructions importantes
- Informations de contact

## Désactivation

Pour désactiver l'envoi d'emails, vous pouvez :
1. Ne pas configurer les variables d'environnement email
2. Ou passer `send_email=False` lors de l'appel à `create_event()`
