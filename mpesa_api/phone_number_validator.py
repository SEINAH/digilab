from django.core.exceptions import ValidationError

def validate_safaricom_number(phone_number):
    # Ensure the phone number is a string
    phone_number = str(phone_number)

    # Ensure the phone number starts with "07" and has exactly 10 digits
    if not phone_number.startswith("07") or len(phone_number) != 10:
        raise ValidationError("Phone number must start with '07' and be 10 digits long")
