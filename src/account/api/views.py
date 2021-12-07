import re
from django.http.response import HttpResponseBadRequest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from account.models import Account
from account.api.serializers import *

@api_view(['POST',])
def registration_view(request):
    if request.method =='POST':
        serializer = RegisterationSerializer(data =request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response'] ='sucessfully registered'
            data['emails'] =account.email
            data['username'] =account.username
            token = Token.objects.get(user=account).key
            data['token']=token 
        else:
            serializer.errors
        return Response(data)
            
@api_view(['GET',])
@permission_classes(IsAuthenticated,)
def account_properties_view(request):
    try:
        account=request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)
    
        
@api_view(['PUT',])
@permission_classes(IsAuthenticated,)
def update_account__view(request):
    try:
        account=request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data['response']= 'account update is sucessfull'
            return Response(data=data)
        return Response(serializer.errors , status=status.HTTP_404_NOT_FOUND)
     