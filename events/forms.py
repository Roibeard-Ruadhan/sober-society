from django import forms
from django.forms import ModelForm
from .models import events
# from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


class EventForm(ModelForm):
    class Meta:
        model = events

        fields = ('location', 'venue', 'venue_image', 'event_date', 'description')

        labels = {
            'venue_image': 'venue_image',
        }
        widgets = {
            'event_date': forms.DateInput
            (attrs={'type': 'date', 'placeholder': 'Date'}),
        }
