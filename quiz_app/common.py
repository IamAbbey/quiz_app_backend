import os
from django.core.mail import send_mail
from django.contrib.auth.models import User


def custom_send_mail(subject, message, list_of_email):
    send_mail(
        subject=subject,
        message=message,
        from_email= os.getenv("DEFAULT_FROM_EMAIL", "info@example.com"),
        recipient_list=list_of_email,
        fail_silently=False,
    )