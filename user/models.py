from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,Group,Permission

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='customuser_set',
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )