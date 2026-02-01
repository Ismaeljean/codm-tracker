from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
]
