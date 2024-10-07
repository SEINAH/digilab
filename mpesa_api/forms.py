from django import forms
from .phone_number_validator import validate_safaricom_number

class MpesaPaymentForm(forms.Form):
    phone_number = forms.CharField(
        max_length=10,
        validators=[validate_safaricom_number],
        help_text="Enter phone number in the format 07XXXXXXXX"
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount
