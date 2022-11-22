from django import forms
from .models import Contact_mails


class ContactForm(forms.ModelForm):
    """
    Creates a contact form
    """
    class Meta:
        model = Contact_mails

        fields = ('full_name', 'email', 'subject', 'message',)

    def __init__(self, *args, **kwargs):
        """ Add placeholders and required attribute,
        set autofocus on first field """
        super().__init__(*args, **kwargs)
        labels = {
            'full_name': 'Full Name',
            'email': 'Email',
            'subject': 'Subject',
            'message': 'Your message'
        }
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].label = labels[field] + ""
            if self.fields[field].required:
                placeholder = f'{labels[field]} *'
            else:
                placeholder = labels[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
