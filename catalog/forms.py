import datetime

from django import forms
from .models import Borrower
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _




# newusers/forms.py

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
"""
#from .models import Borrower
class BorrowerForm(forms.ModelForm)
    class Meta:
        model = Borrower
        fields =("django_id","name","whatsapp","facebook","email_field","address","contact_no","home_no","identy","image")
"""
