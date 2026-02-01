# CODMTracker/middleware.py
# Middleware pour gérer les erreurs 404 et 500
from django.http import Http404
from django.shortcuts import render

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Si c'est une 404 et DEBUG=True, on force notre template
        if response.status_code == 404:
            return render(request, '404.html', status=404)

        return response

class Custom500Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Si c'est une 500 et DEBUG=True, on force notre template
        if response.status_code == 500:
            return render(request, '500.html', status=500)

        return response