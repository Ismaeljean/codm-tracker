from django.shortcuts import render
from .utils.valider_numero import valider_et_normaliser_numero
from .utils.sendmail import send_otp_email
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from .models import Utilisateur, OtpCode


def generate_otp():
    return str(random.randint(100000, 999999))

# Create your views here.
def login_view(request):
    """
    Connexion de l'utilisateur.
    - Rôle: Authentifier l'utilisateur avec email ou numéro de téléphone.
    - URL: path('login/', views.login_view, name='login')
    - Template: utilisateurs/login.html
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        raw_identifiant = request.POST.get('identifiant', '').strip()
        password = request.POST.get('password', '')

        if not raw_identifiant or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'utilisateurs/login.html')

        # Essayer d'abord avec l'email
        try:
            user = Utilisateur.objects.get(email__iexact=raw_identifiant)
            authenticated_user = authenticate(request, username=user.email, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                next_url = request.POST.get('next') or request.GET.get('next') or '/'
                return redirect(next_url)
            else:
                messages.error(request, "Mot de passe incorrect.")
                return render(request, 'utilisateurs/login.html')
        except Utilisateur.DoesNotExist:
            pass

        # Si pas trouvé par email, essayer avec le numéro
        numero = valider_et_normaliser_numero(raw_identifiant)
        if numero:
            try:
                user_obj = Utilisateur.objects.get(numero=numero)
                authenticated_user = authenticate(request, username=user_obj.email, password=password)
                if authenticated_user:
                    login(request, authenticated_user)
                    next_url = request.POST.get('next') or request.GET.get('next') or '/'
                    return redirect(next_url)
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Utilisateur.DoesNotExist:
                messages.error(request, "Aucun compte trouvé pour cet identifiant.")
        else:
            messages.error(request, "Identifiant invalide. Utilisez votre email ou numéro de téléphone.")

    return render(request, 'utilisateurs/login.html', {
        'next': request.GET.get('next', ''),
    })
    
def signup_view(request):
    """
    Inscription de l'utilisateur en 2 étapes.
    - Étape 1 : nom, prénom, email, numéro → envoie code OTP
    - Étape 2 : code OTP + mot de passe → création du compte
    """
    signup_data = request.session.get('signup_data')
    show_otp_form = signup_data is not None

    # Nettoyage session expirée
    if request.session.get('_session_start_time'):
        try:
            start_time = timezone.datetime.fromisoformat(request.session['_session_start_time'].replace('Z', '+00:00'))
            if timezone.now() - start_time > timedelta(minutes=15):
                request.session.pop('signup_data', None)
                request.session.pop('_session_start_time', None)
                signup_data = None
                show_otp_form = False
                messages.info(request, "Votre session a expiré. Veuillez recommencer l'inscription.")
        except:
            pass

    if request.method == 'POST':
        action = request.POST.get('action')

        # ÉTAPE 1 : Réception des infos (nom, prénom, email, numéro)
        if action == 'step1':
            nom = request.POST.get('nom', '').strip()
            prenom = request.POST.get('prenom', '').strip()
            email = request.POST.get('email', '').strip().lower()
            raw_numero = request.POST.get('numero', '').strip()

            # Validations
            if not all([nom, prenom, email, raw_numero]):
                messages.error(request, "Tous les champs sont obligatoires.")
                return render(request, 'utilisateurs/signup.html', {'show_otp_form': False})

            numero = valider_et_normaliser_numero(raw_numero)
            if not numero:
                messages.error(request, "Numéro invalide. Format attendu : +225XXXXXXXXXX")
                return render(request, 'utilisateurs/signup.html', {'show_otp_form': False})

            # Vérifier si l'email existe déjà
            if Utilisateur.objects.filter(email__iexact=email).exists():
                messages.error(request, "Cet email est déjà utilisé.")
                return render(request, 'utilisateurs/signup.html', {'show_otp_form': False})

            # Vérifier si le numéro existe déjà
            if Utilisateur.objects.filter(numero=numero).exists():
                messages.error(request, "Ce numéro est déjà utilisé.")
                return render(request, 'utilisateurs/signup.html', {'show_otp_form': False})

            # Générer et envoyer le code OTP
            code = generate_otp()
            email_envoye = send_otp_email(email, code)

            if not email_envoye:
                messages.error(request, "Impossible d'envoyer le code. Réessayez.")
                return render(request, 'utilisateurs/signup.html', {'show_otp_form': False})

            # Stockage en session (sans mot de passe pour l'instant)
            request.session['signup_data'] = {
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'numero': numero,
            }
            request.session['_session_start_time'] = timezone.now().isoformat()
            request.session.set_expiry(900)  # 15 minutes
            request.session.modified = True

            # Créer le code OTP
            OtpCode.objects.create(numero=numero, code=code)

            messages.success(request, f"Code de vérification envoyé à {email} !")
            return render(request, 'utilisateurs/signup.html', {
                'show_otp_form': True,
                'signup_data': request.session['signup_data']
            })

        # ÉTAPE 2 : Vérification du code OTP + mot de passe
        elif action == 'step2':
            data = request.session.get('signup_data')
            if not data:
                messages.error(request, "Session expirée. Veuillez recommencer l'inscription.")
                return redirect('utilisateurs:signup')

            code = request.POST.get('code', '').strip()
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            # Validation du code
            if not code.isdigit() or len(code) != 6:
                messages.error(request, "Le code doit contenir 6 chiffres.")
                return render(request, 'utilisateurs/signup.html', {
                    'show_otp_form': True,
                    'signup_data': data
                })

            # Vérifier le code OTP
            otp_exists = OtpCode.objects.filter(numero=data['numero'], code=code).exists()
            if not otp_exists:
                messages.error(request, "Code incorrect ou expiré.")
                return render(request, 'utilisateurs/signup.html', {
                    'show_otp_form': True,
                    'signup_data': data
                })

            # Validation des mots de passe
            if not password1 or not password2:
                messages.error(request, "Les mots de passe sont obligatoires.")
                return render(request, 'utilisateurs/signup.html', {
                    'show_otp_form': True,
                    'signup_data': data
                })

            if password1 != password2:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return render(request, 'utilisateurs/signup.html', {
                    'show_otp_form': True,
                    'signup_data': data
                })

            if len(password1) < 6:
                messages.error(request, "Le mot de passe doit contenir au moins 6 caractères.")
                return render(request, 'utilisateurs/signup.html', {
                    'show_otp_form': True,
                    'signup_data': data
                })

            # Création du compte
            try:
                user = Utilisateur(
                    nom=data['nom'],
                    prenom=data['prenom'],
                    email=data['email'],
                    numero=data['numero'],
                    is_active=True,
                )
                user.set_password(password1)
                user.save()

                # Nettoyer la session
                request.session.pop('signup_data', None)
                request.session.pop('_session_start_time', None)

                # Connecter l'utilisateur
                login(request, user)

                messages.success(request, "Compte créé avec succès ! Créez maintenant votre profil joueur.")
                return redirect('profils:create_profil')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de la création du compte. Veuillez réessayer.")
                return render(request, 'utilisateurs/signup.html', {
                    'show_otp_form': True,
                    'signup_data': data
                })

    return render(request, 'utilisateurs/signup.html', {
        'show_otp_form': show_otp_form,
        'signup_data': signup_data or {}
    })


def resend_otp_view(request):
    """
    Renvoyer un nouveau code OTP pendant l'inscription.
    - Rôle: Envoyer un nouveau code OTP à l'utilisateur.
    - URL: path('resend_otp/', views.resend_otp_view, name='resend_otp')
    """
    if request.method != 'POST':
        return redirect('utilisateurs:signup')

    data = request.session.get('signup_data')
    if not data:
        messages.error(request, "Aucune inscription en cours.")
        return redirect('utilisateurs:signup')

    code = generate_otp()
    numero = data['numero']
    email = data['email']

    email_envoye = send_otp_email(email, code)
    
    if email_envoye:
        OtpCode.objects.create(numero=numero, code=code)
        messages.success(request, f"Nouveau code envoyé à {email} !")
    else:
        messages.error(request, "Impossible d'envoyer le code. Réessayez.")
    
    return redirect('utilisateurs:signup')

def forgot_password_view(request):
    """
    Mot de passe oublié → 3 étapes dans une seule view
    action=email → otp → reset
    """

    step = "email"  # étape par défaut
    email = request.session.get('fp_email')

    if request.method == "POST":
        action = request.POST.get("action")

        # 📩 ÉTAPE 1 — RECEVOIR EMAIL
        if action == "email":
            email = request.POST.get("email", "").strip().lower()

            if not email:
                messages.error(request, "Email obligatoire.")
                return render(request, "utilisateurs/forgot_password.html", {"step": "email"})

            try:
                user = Utilisateur.objects.get(email=email)
            except Utilisateur.DoesNotExist:
                messages.error(request, "Aucun compte associé à cet email.")
                return render(request, "utilisateurs/forgot_password.html", {"step": "email"})

            code = generate_otp()
            send_otp_email(email, code)

            OtpCode.objects.create(numero=email, code=code)  # numero peut être un email pour forgot_password

            request.session['fp_email'] = email
            step = "otp"
            messages.success(request, "Code envoyé à votre email.")
            return render(request, "utilisateurs/forgot_password.html", {"step": step, "email": email})

        # 🔐 ÉTAPE 2 — VÉRIFICATION OTP
        if action == "otp":
            code = request.POST.get("code", "").strip()

            if not email:
                messages.error(request, "Session expirée.")
                return redirect("utilisateurs:forgot_password")

            if not OtpCode.objects.filter(numero=email, code=code).exists():
                messages.error(request, "Code incorrect ou expiré.")
                return render(request, "utilisateurs/forgot_password.html", {"step": "otp", "email": email})

            request.session['fp_code_ok'] = True
            step = "reset"
            messages.success(request, "Code vérifié. Choisissez un nouveau mot de passe.")
            return render(request, "utilisateurs/forgot_password.html",
                          {"step": step, "email": email})

        # 🔁 RENVOYER OTP
        if action == "resend":
            code = generate_otp()
            send_otp_email(email, code)
            OtpCode.objects.create(numero=email, code=code)
            messages.success(request, "Nouveau code envoyé.")
            return render(request, "utilisateurs/forgot_password.html", {"step": "otp", "email": email})

        # 🔑 ÉTAPE 3 — RÉINITIALISATION DU MDP
        if action == "reset":
            if not request.session.get('fp_code_ok'):
                messages.error(request, "Vérifiez d'abord votre code OTP.")
                return redirect("utilisateurs:forgot_password")

            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return render(request, "utilisateurs/forgot_password.html", {"step": "reset"})

            if len(password1) < 6:
                messages.error(request, "Mot de passe trop court (6 caractères min).")
                return render(request, "utilisateurs/forgot_password.html", {"step": "reset"})

            user = Utilisateur.objects.get(email=email)
            user.set_password(password1)
            user.save()

            # Nettoyer la session
            request.session.pop('fp_email', None)
            request.session.pop('fp_code_ok', None)

            messages.success(request, "Mot de passe mis à jour. Connectez-vous.")
            return redirect("utilisateurs:login")

    return render(request, "utilisateurs/forgot_password.html", {"step": step})

def logout_view(request):
    """
    Déconnexion de l'utilisateur.
    - Rôle: Déconnecter l'utilisateur et rediriger vers l'accueil.
    - URL: path('logout/', views.logout_view, name='logout')
    """
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('/')
