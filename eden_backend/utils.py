from django.core.mail import get_connection, EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Util:
    @staticmethod
    def send_email(data):
        try:
            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
                timeout=getattr(settings, "EMAIL_TIMEOUT", 30),
            )
            # optionally set debug level on underlying connection for dev
            # connection.open()  # optional; get_connection() will open when needed

            email = EmailMessage(
                subject=data['email_subject'],
                body=data['email_body'],
                from_email=settings.EMAIL_HOST_USER,
                to=[data['to_email']],
                connection=connection
            )
            email.send(fail_silently=False)
        except Exception as e:
            logger.exception("Failed to send email")
            raise
