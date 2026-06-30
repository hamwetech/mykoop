import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from conf.utils import log_debug
from messaging.models import SmsLog
from messaging.api.hamwesms import MessagingOperations
from conf.models import SystemConfiguration

sms = MessagingOperations()


def send_email_with_footer(to_email, subject, content):
    """
    Send email with a standard footer using HTML template
    """
    try:
        html_body = render_to_string(
            "emails/base_email.html",
            {"content": content}
        )

        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )

        email.content_subtype = "html"  # important!

        email.send()

        log_debug(f"Email sent to {to_email}")
        return {"status": "SUCCESS"}

    except Exception as e:
        log_debug(f"Email error: {e}", exc_info=True)
        return {"status": "FAILED", "error": str(e)}


def send_sms(recipient: str, message: str, sender: str = None):
    try:

        conf = SystemConfiguration.objects.all().first()
        if not conf.send_sms:
            log_debug('SMS is not enabled')
            return

        payload = {
            "to": recipient,
            "message": message,
            "sender": sender
        }

        response = sms.send_message(recipient, message)
        status = "SUCCESS" if response == "SUCCESS" else "FAILED"

        # Log SMS attempt
        SmsLog.objects.create(
            recipient=recipient,
            message=message,
            status=status,
            api_response=response,
            sender=sender
        )

        return response

    except Exception as e:
        # Log exception
        SmsLog.objects.create(
            recipient=recipient,
            message=message,
            status="ERROR",
            error=str(e),
            sender=sender
        )
        raise e