from rest_framework import serializers
from .models import CustomUser
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    password2=serializers.CharField(required=True,write_only=True)
    email=serializers.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'image','password','password2')



    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
        )        
        user.set_password(validated_data['password'])
        user.save()
        return  user