from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,Group,Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_set')
    follower=models.ManyToManyField('self',symmetrical=False,related_name="follow")

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='customuser_set',
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    @property
    def followers(self):
        count=self.follower.all()
        return len(count)



    @property
    def following(self):
        user=CustomUser.objects.get(pk=self.pk)
        count=CustomUser.objects.filter(follower=user)

        return len(count)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)