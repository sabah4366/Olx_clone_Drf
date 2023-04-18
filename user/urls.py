
from django.urls import path
from .views import UserList
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('users/', UserList.as_view()),
]
urlpatterns=format_suffix_patterns(urlpatterns)