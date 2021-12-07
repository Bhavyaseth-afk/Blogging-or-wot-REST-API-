import re
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

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
            