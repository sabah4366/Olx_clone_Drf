from rest_framework import serializers
from .models import CustomUser
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    password2=serializers.CharField(required=True,write_only=True)
    email=serializers.CharField(required=True)
    followers=serializers.CharField(read_only=True)
    following=serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'first_name','last_name','image','password','password2','followers','following')


    
    def validate(self, attrs):
        email=attrs['email']
        phone_number=attrs['phone_number']
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error":'email already exists'})

        if CustomUser.objects.filter(phone_number=phone_number).exists():
             raise serializers.ValidationError({"error":'phone number already exists'})
           
        if attrs['password'] and ['password2']:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"error": "Password fields didn't match."})
            return attrs

    def create(self, validated_data):
        # the pop() method is used to retrieve the value of the 'password' key from the validated_data dictionary and remove it from the dictionary. 
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        user = CustomUserSerializer(**validated_data)
        # set_password() method will hash the password before saving password into database
        user.set_password(password)
        user.save()
        return user

class UserUpdateSeerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields= ('id', 'username', 'email', 'phone_number', 'first_name','last_name','image')

             