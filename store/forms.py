import re

from django import forms


class CheckoutForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "10-digit phone number"}),
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3,
                                     "placeholder": "Delivery address"}),
    )
    # Filled in by JavaScript from the browser cart: [{"id": 1, "qty": 2}, ...]
    cart = forms.CharField(widget=forms.HiddenInput)

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_phone(self):
        digits = re.sub(r"\D", "", self.cleaned_data["phone"])
        if not 10 <= len(digits) <= 15:
            raise forms.ValidationError("Enter a valid phone number (at least 10 digits).")
        return digits
