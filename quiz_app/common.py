from django.core.mail import send_mail
from django.contrib.auth.models import User


def custom_send_mail(subject, message, list_of_email):
    send_mail(
        subject,
        message,
        'from@example.com',
        list_of_email,
        fail_silently=False,
    )