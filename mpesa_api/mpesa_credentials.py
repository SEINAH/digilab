import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MpesaC2bCredential:
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    api_URL = os.getenv('MPESA_API_URL')

class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

class LipanaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = os.getenv('BUSINESS_SHORT_CODE')
    passkey = os.getenv('MPESA_PASSKEY')

    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
