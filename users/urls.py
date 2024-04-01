from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in_view, name='sign_in'),  # Update to sign_in_view
    path('sign_out/', views.sign_out, name='sign_out'),  # Sign-out URL
]
