from django.db import models
from django.utils import timezone


class Contact_mails(models.Model):
    """
    A model to create a contact message which includes
    the user, their email, the message
    & the date it's sent
    """

    class Meta:
        verbose_name_plural = 'Contact Emails'

    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=80, null=False, blank=False)
    subject = models.CharField(max_length=254, null=False, blank=False)
    message = models.TextField(blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject
