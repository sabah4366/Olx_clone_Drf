from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from .models import CustomUser
from django.http import Http404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
class UserList(APIView):
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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