from django.urls import path    
from .views import home, profile, user_create, user_delete

urlpatterns =[
    path('', home, name='home'),
    path('register/', user_create, name='user_create'),
    path('profile/<pk>/', profile, name='users-profile'),
    path('profile/<pk>/delete', user_delete, name='user-delete'),   
]