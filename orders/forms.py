
import re

from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone']

    def clean_customer_name(self):
        name = self.cleaned_data['customer_name'].strip()

        if not name:
            raise forms.ValidationError(
                "Please enter your name."
            )

        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()

        if not re.fullmatch(r'\+?[0-9\s().-]+', phone):
            raise forms.ValidationError(
                "Enter a valid phone number."
            )

        digits = re.sub(r'\D', '', phone)

        if not 7 <= len(digits) <= 15:
            raise forms.ValidationError(
                "Phone number must contain between 7 and 15 digits."
            )

        return phone
