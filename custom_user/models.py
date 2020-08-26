from django.db import models
from quiz_app.common import custom_send_mail
from django.contrib.auth.models import User

# Create your models here.
class EmailRecord(models.Model):

    subject = models.CharField(max_length=220)
    message = models.TextField()
    no_of_user = models.PositiveSmallIntegerField(
        help_text="The number of users as at the time this mail was sent"
    )
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        """
        Sends mail to all active available users, and then eventually save
        the mail for record purposes
        """
        user_email_list = list(
            User.objects.filter(
                is_active=True, is_staff=False, is_superuser=False
            ).values_list("email", flat=True)
        )
        self.no_of_user = len(user_email_list)
        custom_send_mail(
            subject=self.subject, message=self.message, list_of_email=user_email_list
        )
        super(EmailRecord, self).save(*args, **kwargs)
