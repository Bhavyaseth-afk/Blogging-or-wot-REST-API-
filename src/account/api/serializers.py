from rest_framework import fields, serializers

from account.models import Account



class RegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	
    class Meta:
        model = Account
        fields = ['email', 'username', 'password','password2']
        extra_kwarg ={
            'password':{'write_only':True}
        }


    def save(self):
        account = Account(
            email = self.validated_data['email'],
            username =self.validated_data['username']
        )
        password= self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Passowrds dont match'})
        account.set_password(password)
        account.save()
        return account
            




class AccountPropertiesSerializer(serializers.Serializer):
    
    class Meta:
        model =Account
        fields = {'email' ,'username', 'pk'}