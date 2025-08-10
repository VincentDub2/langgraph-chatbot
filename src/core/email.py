"""
Module pour l'envoi d'emails de confirmation de rendez-vous
"""
import os
from typing import List, Dict, Optional
from datetime import datetime
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from .config import get_settings


class EmailService:
    """Service d'envoi d'emails"""
    
    def __init__(self):
        self.settings = get_settings()
        self.config = ConnectionConfig(
            MAIL_USERNAME=self.settings.mail_username,
            MAIL_PASSWORD=self.settings.mail_password,
            MAIL_FROM=self.settings.mail_from,
            MAIL_PORT=self.settings.mail_port,
            MAIL_SERVER=self.settings.mail_server,
            MAIL_STARTTLS=self.settings.mail_starttls,
            MAIL_SSL_TLS=self.settings.mail_ssl_tls,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.fastmail = FastMail(self.config)
    
    async def send_appointment_confirmation(
        self,
        client_email: str,
        client_name: str,
        appointment_data: Dict,
        agent_name: str = "Notre agent"
    ) -> bool:
        """
        Envoie un email de confirmation de rendez-vous
        
        Args:
            client_email: Email du client
            client_name: Nom du client
            appointment_data: Données du rendez-vous
            agent_name: Nom de l'agent
            
        Returns:
            bool: True si l'email a été envoyé avec succès
        """
        try:
            # Formatage de la date
            start_dt = datetime.fromisoformat(appointment_data["start_iso"])
            end_dt = datetime.fromisoformat(appointment_data["end_iso"])
            
            # Création du contenu de l'email
            subject = f"Confirmation de votre rendez-vous - {appointment_data.get('title', 'Visite')}"
            
            html_content = self._create_confirmation_html(
                client_name=client_name,
                appointment_data=appointment_data,
                start_dt=start_dt,
                end_dt=end_dt,
                agent_name=agent_name
            )
            
            text_content = self._create_confirmation_text(
                client_name=client_name,
                appointment_data=appointment_data,
                start_dt=start_dt,
                end_dt=end_dt,
                agent_name=agent_name
            )
            
            message = MessageSchema(
                subject=subject,
                recipients=[client_email],
                body=html_content,
                subtype="html"
            )
            
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {e}")
            return False
    
    def _create_confirmation_html(
        self,
        client_name: str,
        appointment_data: Dict,
        start_dt: datetime,
        end_dt: datetime,
        agent_name: str
    ) -> str:
        """Crée le contenu HTML de l'email de confirmation"""
        
        location = appointment_data.get("location", "Lieu à confirmer")
        description = appointment_data.get("description", "")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .details {{ background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 5px; padding: 20px; }}
                .detail-row {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #495057; }}
                .value {{ color: #212529; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; font-size: 14px; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>✅ Confirmation de votre rendez-vous</h2>
                    <p>Bonjour {client_name},</p>
                    <p>Votre rendez-vous a été confirmé avec succès !</p>
                </div>
                
                <div class="details">
                    <h3>Détails du rendez-vous</h3>
                    
                    <div class="detail-row">
                        <span class="label">Sujet :</span>
                        <span class="value">{appointment_data.get('title', 'Visite')}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="label">Date :</span>
                        <span class="value">{start_dt.strftime('%A %d %B %Y')}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="label">Heure :</span>
                        <span class="value">{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="label">Lieu :</span>
                        <span class="value">{location}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="label">Agent :</span>
                        <span class="value">{agent_name}</span>
                    </div>
        """
        
        if description:
            html += f"""
                    <div class="detail-row">
                        <span class="label">Description :</span>
                        <span class="value">{description}</span>
                    </div>
            """
        
        html += """
                </div>
                
                <div class="footer">
                    <p><strong>Important :</strong></p>
                    <ul>
                        <li>Merci d'arriver 5 minutes avant l'heure prévue</li>
                        <li>En cas d'impossibilité, merci de nous contacter au plus tôt</li>
                        <li>N'oubliez pas d'apporter les documents nécessaires</li>
                    </ul>
                    
                    <p>Pour toute question, n'hésitez pas à nous contacter.</p>
                    
                    <p>Cordialement,<br>
                    L'équipe de votre agence immobilière</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _create_confirmation_text(
        self,
        client_name: str,
        appointment_data: Dict,
        start_dt: datetime,
        end_dt: datetime,
        agent_name: str
    ) -> str:
        """Crée le contenu texte de l'email de confirmation"""
        
        location = appointment_data.get("location", "Lieu à confirmer")
        description = appointment_data.get("description", "")
        
        text = f"""
Confirmation de votre rendez-vous

Bonjour {client_name},

Votre rendez-vous a été confirmé avec succès !

DÉTAILS DU RENDEZ-VOUS :
- Sujet : {appointment_data.get('title', 'Visite')}
- Date : {start_dt.strftime('%A %d %B %Y')}
- Heure : {start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}
- Lieu : {location}
- Agent : {agent_name}
"""
        
        if description:
            text += f"- Description : {description}\n"
        
        text += """
IMPORTANT :
- Merci d'arriver 5 minutes avant l'heure prévue
- En cas d'impossibilité, merci de nous contacter au plus tôt
- N'oubliez pas d'apporter les documents nécessaires

Pour toute question, n'hésitez pas à nous contacter.

Cordialement,
L'équipe de votre agence immobilière
"""
        
        return text


# Instance globale du service email
email_service = EmailService()
