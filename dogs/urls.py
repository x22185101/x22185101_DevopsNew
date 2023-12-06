from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', include('users.urls')),
    path('signin/', auth_views.LoginView.as_view(template_name='users/signin.html'), name='sign_in'),
    path('signout/', auth_views.LogoutView.as_view(template_name='users/signout.html'), name='sign_out'),
    path('', include('animal_shelter.urls')),
    path('pet_products/', include('pet_products.urls')),
]
