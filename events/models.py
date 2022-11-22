from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class events(models.Model):
    # organiser = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    location = models.CharField(max_length=150, unique=False)
    venue = models.CharField(max_length=150, unique=False)
    venue_image = CloudinaryField(
        'image', default='https://res.cloudinary.com/roibeard/image/upload/v1655578160/placeholder.jpg')
    event_date = models.DateField('Event Date', blank=True, null=True)
    description = models.TextField(blank=True, max_length=200)
    approve = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events_creator", null=True
    )
    guests = models.ManyToManyField(
        User, related_name='events_guests', blank=True)

    def number_of_guests(self):
        return self.guests.count()

    def __str__(self):
        return self.location


# Events plural in the admin
    class Meta:
        verbose_name_plural = "Event"
