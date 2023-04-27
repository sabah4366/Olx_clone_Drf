from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomUserSerializer,UserUpdateSeerializer
from .models import CustomUser
from django.http import Http404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.shortcuts import get_object_or_404

class UserList(APIView):
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            profile_pic = request.FILES.get('image', None)
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data.get('first_name',None)
            last_name = serializer.validated_data.get('last_name',None)
            phone_number=serializer.validated_data.get('phone_number',None)
            password2 = request.data.get('password2', None)
            if password != password2:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
    
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if phone_number:
                user.phone_number=phone_number
            if profile_pic:
                user.image = profile_pic
            user.save()
            serialized_user = CustomUserSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self,pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        user=self.get_object(pk)
        serializer=CustomUserSerializer(user,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def patch(self,request,pk):
        instance=self.get_object(pk)        
        if instance == self.request.user:
            if 'id' in request.data:
                return Response(data={"error":"cannot change the user id"},status=status.HTTP_400_BAD_REQUEST)
            if 'username' in request.data:
                return Response(data={"error":"cannot change the username"},status=status.HTTP_400_BAD_REQUEST)

            user=CustomUser.objects.get(pk=pk)
            if 'email' in request.data:
                request_email=request.data['email']
                user_email=user.email
                if request_email != user_email:
                    if CustomUser.objects.filter(email=request_email).exists():
                        return Response(data={"error":"email already exists"},status=status.HTTP_400_BAD_REQUEST)

            if 'phone_number' in request.data:
                request_phone_number=request.data['phone_number']
                user_phone_number=user.phone_number
                if request_phone_number != user_phone_number:
                    if CustomUser.objects.filter(phone_number=request_phone_number).exists():
                        return Response(data={"error":"phone number already exists"},status=status.HTTP_400_BAD_REQUEST)
 
            serializer=UserUpdateSeerializer(instance,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response(data={"error":"permission denied for this user"},status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk):
        user=get_object_or_404(CustomUser,pk=pk)
        if user == self.request.user:
            user.delete()
            return Response('deleted',status=status.HTTP_200_OK)
        else: 
            return Response({"error":"permission denied for this user"},status=status.HTTP_400_BAD_REQUEST)
            

    

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_name': user.username,
            'email': user.email
        })

class AddFollower(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,pk):
        try:
            user=CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
        if user != request.user:
            if user.follower.filter(id=request.user.id):
                user.follower.remove(request.user)
                user.save()
                return Response(data=f"you are unfollowed by-{user}")
            else:
                user.follower.add(request.user)
                user.save()
                return Response(data=f"you are followed by-{user}")
        else:
            return Response(data="you are logined user and also as a follower user")