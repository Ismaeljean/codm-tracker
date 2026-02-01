# commande/utils/sendmail.py → VERSION FINALE SANS IMAGE (à copier-coller entièrement)
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

logger = logging.getLogger(__name__)

def _get_email_subject() -> str:
    return "Votre code de vérification CODM Tracker"

def _get_email_html_template(otp_code: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Code CODM Tracker</title>
        <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{ font-family:'Segoe UI',Arial,sans-serif; background:#f7f7f7; color:#333; }}
            .container {{ max-width:600px; margin:30px auto; background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.08); }}
            .header {{ background:linear-gradient(135deg, #dc3545, #ff6b35); padding:40px 30px; text-align:center; color:white; }}
            .header h1 {{ font-size:32px; font-weight:700; margin:0; letter-spacing:1px; }}
            .header p {{ margin:10px 0 0; font-size:17px; opacity:0.95; }}
            .content {{ padding:50px 40px; text-align:center; }}
            .otp {{ 
                display:inline-block; 
                background:#fff5f5; 
                color:#dc3545; 
                font-size:52px; 
                font-weight:800; 
                letter-spacing:14px; 
                padding:25px 50px; 
                border:3px solid #ffe0e0; 
                border-radius:16px; 
                margin:30px 0; 
                font-family:'Courier New', monospace;
                box-shadow:0 6px 20px rgba(220,53,69,0.15);
            }}
            .text {{ color:#555; font-size:17px; line-height:1.7; margin:25px 0; }}
            .highlight {{ color:#dc3545; font-weight:600; }}
            .footer {{ background:#f1f3f5; padding:30px; text-align:center; font-size:13px; color:#777; }}
            .footer a {{ color:#dc3545; text-decoration:none; }}
            @media (max-width:600px) {{
                .container {{ border-radius:0; margin:0; }}
                .header, .content {{ padding-left:20px; padding-right:20px; }}
                .otp {{ font-size:40px; letter-spacing:8px; padding:20px 30px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- En-tête rouge/orange signature CODM Tracker -->
            <div class="header">
                <h1>CODM Tracker</h1>
                <p>Vérification de votre compte</p>
            </div>

            <!-- Corps -->
            <div class="content">
                <h2 style="color:#222; margin-bottom:25px; font-size:26px; font-weight:normal;">
                    Voici votre code de sécurité
                </h2>

                <div class="otp">{otp_code}</div>

                <p class="text">
                    Ce code est valable pendant <span class="highlight">15 minutes</span>.<br>
                    Si vous n'avez pas demandé cette vérification, ignorez cet email.
                </p>
            </div>

            <!-- Pied de page -->
            <div class="footer">
                <p>© {timezone.now().year} <strong>CODM Tracker</strong> • Tous droits réservés</p>
                <p>
                    Besoin d’aide ? Contactez-nous : 
                    <a href="mailto:contact@codmtracker.com">contact@codmtracker.com</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

def _get_email_text_template(otp_code: str) -> str:
    return f"""
Votre code de vérification CODM Tracker : {otp_code}

Ce code expire dans 15 minutes.
Ne partagez jamais ce code.

© {timezone.now().year} CODM Tracker - Tous droits réservés
    """.strip()

def send_otp_email(recipient_email: str, otp_code: str) -> bool:
    try:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@codmtracker.com')
        msg = EmailMultiAlternatives(
            subject=_get_email_subject(),
            body=_get_email_text_template(otp_code),
            from_email=from_email,
            to=[recipient_email],
        )
        msg.attach_alternative(_get_email_html_template(otp_code), "text/html")
        msg.send()
        logger.info(f"Email OTP envoyé à {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Échec envoi email OTP : {e}")
        return False