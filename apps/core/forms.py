import re

from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "inquiry_type",
            "full_name",
            "company_name",
            "phone",
            "email",
            "city",
            "product_interest",
            "quantity",
            "message",
        ]

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if len(re.sub(r"\D", "", phone)) < 10:
            raise forms.ValidationError("Enter a valid mobile number.")
        return phone
