from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    # Use a datetime-local widget to allow easy date/time selection.
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'location']
