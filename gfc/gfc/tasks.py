from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import calendar
from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import datetime
from django.conf import settings


def send_monthly_newsletter_email():
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        context ={
            "user":user,
            "month": calendar.month_name[datetime.now(tz=None).month]
        }
        html_content = render_to_string("partials/monthly_newsletter.html", context)
        text_content = strip_tags(html_content)
        send_mail(
        'Monthly Newsletter',
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message = html_content,
        fail_silently=False,
        )
    print("EMAILS SENT")
        