from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),  # Sign-out URL
]