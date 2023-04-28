
from django.urls import path
from .views import UserList,CustomAuthToken,AddFollower,UserDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('register/', UserList.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('user/<int:pk>/',UserDetailView.as_view()),
    path('user/<int:pk>/follow/',AddFollower.as_view()),
]
urlpatterns=format_suffix_patterns(urlpatterns)