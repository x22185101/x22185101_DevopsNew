from django.contrib.auth.views import LoginView
from django.shortcuts import render

class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Hi {self.request.user.username}!')
        return response
