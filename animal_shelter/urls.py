from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'animal_shelter'

urlpatterns = [
   
    path('', views.index, name='index'),
   
    path('<int:animal_shelter_id>/', views.show, name='show'),
    
    path('category/<str:category>/', views.category, name='category'),
   
    
    path('adopt/', views.adopt, name='adopt'),
    path('adoption-policy/', views.adoption_policy, name='adoption_policy'),
    path('products/', views.product_list, name='product_list'),
    path('create_animal/', views.user_create_animal, name='user_create_animal'),
    path('update_animal/<int:animal_shelter_id>/', views.user_update_animal, name='user_update_animal'),
    path('delete_animal/<int:animal_shelter_id>/', views.user_delete_animal, name='user_delete_animal'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')

    
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
