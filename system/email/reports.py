from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date

from conf.utils import send_email_with_logo
from payments.models import Transaction


def send_daily_report():
    context = {
        "date": date.today(),
        "year": date.today().year,
        "total_farmers": 120,
        "total_collections": 45,
        "total_amount": "2,500,000",
        "transactions": Transaction.objects.all()[:10]
    }

    html_content = render_to_string("emails/report.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject="Daily Report",
        body=text_content,
        from_email="tech@hamwe.org",
        to=["geoffrey.w.ndungu@gmail.com"]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

    # send_email_with_logo("TEst", "tech@hamwe.org", "Daily Report")