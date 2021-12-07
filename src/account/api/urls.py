from django.urls import path
from account.api.views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'
urlpatterns = [
    
    path('login' , obtain_auth_token, name='login'),
    path('properties' , account_properties_view, name='properties'),
    path('properties/update' , update_account__view, name='update'),
    path('register' , registration_view, name='register'),
]
 