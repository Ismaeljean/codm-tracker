from .models import Notification


def notifications_count(request):
    """Context processor pour ajouter le nombre de notifications non lues"""
    if request.user.is_authenticated:
        count = Notification.objects.filter(utilisateur=request.user, lu=False).count()
        return {
            'notifications_count': count
        }
    return {
        'notifications_count': 0
    }
