# boutique/utils/paystack.py
import requests
import os
from decimal import Decimal

MODE = os.getenv('PAYSTACK_MODE', 'test').lower()

if MODE == 'live':
    SECRET_KEY = os.getenv('PAYSTACK_LIVE_SECRET_KEY', '')
else:
    SECRET_KEY = os.getenv('PAYSTACK_TEST_SECRET_KEY', '')

# Note: SECRET_KEY peut être vide en développement, mais sera nécessaire pour les paiements

BASE_URL = "https://api.paystack.co"

def initialize_payment(email: str, amount_xof: Decimal, reference: str, callback_url: str, metadata=None, channels=None):
    if not SECRET_KEY:
        print("ERREUR PAYSTACK : Clé secrète manquante. Configurez PAYSTACK_TEST_SECRET_KEY ou PAYSTACK_LIVE_SECRET_KEY dans votre .env")
        return None, None
    
    # Multiplier par 100 pour Paystack (obligatoire même pour XOF sans sous-unité)
    amount_in_subunits = int(amount_xof * 100)

    payload = {
        "email": email,
        "amount": amount_in_subunits,           # Maintenant: 1200 * 100 = 120000
        "currency": "XOF",
        "reference": reference,
        "callback_url": callback_url,
        "metadata": metadata or {}
    }
    if channels:
        payload["channels"] = channels

    try:
        r = requests.post(
            f"{BASE_URL}/transaction/initialize",
            json=payload,
            headers={"Authorization": f"Bearer {SECRET_KEY}"},
            timeout=15
        )
        data = r.json()
        if data.get("status"):
            print(f"PAYSTACK OK → {data['data']['authorization_url']}")
            return data["data"]["authorization_url"], data["data"]["reference"]
        else:
            print(f"PAYSTACK REFUS : {data.get('message')}")
            return None, None
    except Exception as e:
        print(f"ERREUR PAYSTACK : {e}")
        return None, None

def verify_payment(reference: str):
    if not SECRET_KEY:
        print("ERREUR PAYSTACK : Clé secrète manquante. Configurez PAYSTACK_TEST_SECRET_KEY ou PAYSTACK_LIVE_SECRET_KEY dans votre .env")
        return False, None
    
    try:
        r = requests.get(
            f"{BASE_URL}/transaction/verify/{reference}",
            headers={"Authorization": f"Bearer {SECRET_KEY}"},
            timeout=15
        )
        data = r.json()
        if data.get("status") and data["data"]["status"] == "success":
            return True, data["data"]
        return False, None
    except Exception as e:
        print(f"ERREUR VÉRIFICATION : {e}")
        return False, None