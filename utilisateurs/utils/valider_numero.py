# utils.py/valider_numero.py
import re

def valider_et_normaliser_numero(raw_numero):
    """
    Nettoie et formate un numéro ivoirien au format +225XXXXXXXXXX
    Accepte : 0101120890, +2250101120890, 002250101120890, 101120890, +225+2250101120890
    """
    if not raw_numero:
        return None

    # Supprimer tout sauf les chiffres
    numero = re.sub(r'\D', '', raw_numero)

    # Corriger les doublons possibles de préfixe
    while numero.startswith('0022500225'):
        numero = numero.replace('0022500225', '225', 1)
    while numero.startswith('225225'):
        numero = numero.replace('225225', '225', 1)

    # Enlever les préfixes internationaux
    if numero.startswith('00225'):
        numero = numero[5:]
    elif numero.startswith('225'):
        numero = numero[3:]

    # Si le numéro a 8 chiffres → ajouter 0 devant (ancien format)
    if len(numero) == 8:
        numero = '0' + numero
    elif len(numero) == 9 and not numero.startswith('0'):
        numero = '0' + numero

    # ✅ Vérifie que c’est bien un numéro ivoirien mobile valide à 10 chiffres
    if not re.match(r'^0[15789]\d{8}$', numero):
        print("⚠️ Numéro non valide:", numero)
        return None

    # Retourne le format final international
    return f'+225{numero}'
