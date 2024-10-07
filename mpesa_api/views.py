from django.http import JsonResponse
from django.shortcuts import render
import requests
import json
from datetime import datetime
import base64
import os
from dotenv import load_dotenv

from mpesa_api.forms import MpesaPaymentForm
from .models import Transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Load environment variables from .env file
load_dotenv()

#@login_required
def lipa_na_mpesa_online(request):
    from .mpesa_credentials import MpesaAccessToken  # Local import for access token

    if request.method == 'POST':
        form = MpesaPaymentForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            amount = form.cleaned_data['amount']

            # Convert the phone number from "07XXXXXXXX" to "2547XXXXXXXX"
            phone_number = format_phone_number(phone_number)

            if not phone_number:
                return render(request, 'lipa_na_mpesa_online.html', {
                    'form': form,
                    'errors': {'phone_number': 'Invalid phone number format'}
                })

            # Get user info for AccountReference
            user = request.user
            account_reference = f"{user.first_name} {user.last_name}"

            # Access token
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            # Generate new timestamp and password for the request
            lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
            business_short_code = os.getenv('MPESA_BUSINESS_SHORTCODE')
            passkey = os.getenv('MPESA_PASSKEY')
            data_to_encode = f"{business_short_code}{passkey}{lipa_time}"
            online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

            # Payload data for the M-Pesa API
            payload = {
                "BusinessShortCode": business_short_code,
                "Password": online_password,
                "Timestamp": lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": business_short_code,
                "PhoneNumber": phone_number,
                "CallBackURL": os.getenv('MPESA_CALLBACK_URL'),
                "AccountReference": account_reference,
                "TransactionDesc": f"Payment by {account_reference}"
            }

            # Create a new Transaction record
            transaction = Transaction.objects.create(
                user=user,
                transaction_id=account_reference,  # You might use a unique transaction ID from M-Pesa here.
                amount=amount,
                status='pending',
                ip_address=request.META.get('REMOTE_ADDR'),
                time=timezone.now(),
                description=f"Payment by {account_reference}"
            )

            try:
                # Send the request to the M-Pesa API
                response = requests.post(api_url, json=payload, headers=headers)
                response_data = response.json()

                # Handle the response
                if response.status_code == 200:
                    # Update transaction status to 'paid' if successful
                    transaction.status = 'paid'
                    transaction.save()

                    return render(request, 'mpesa/lipa_na_mpesa_online.html', {
                        'form': form,
                        'message': 'Payment processed successfully!',
                        'redirect_url': request.META.get('HTTP_REFERER')  # Redirect to the previous page
                    })
                else:
                    # Update transaction status to 'cancelled' in case of failure
                    transaction.status = 'cancelled'
                    transaction.save()

                    return render(request, 'mpesa/lipa_na_mpesa_online.html', {
                        'form': form,
                        'errors': response_data
                    })

            except requests.exceptions.RequestException as e:
                # Handle network error
                transaction.status = 'cancelled'
                transaction.save()

                return render(request, 'mpesa/lipa_na_mpesa_online.html', {
                    'form': form,
                    'errors': {'general': 'Network error occurred. Please try again later.'}
                })

        else:
            return render(request, 'mpesa/lipa_na_mpesa_online.html', {
                'form': form,
                'errors': form.errors
            })
    else:
        form = MpesaPaymentForm()
        return render(request, 'mpesa/lipa_na_mpesa_online.html', {'form': form})

def format_phone_number(phone_number):
    """Convert phone number from '07XXXXXXXX' to '2547XXXXXXXX'."""
    if phone_number.startswith('0'):
        return "254" + phone_number[1:]
    return None
