from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True,
                              default='defaults/default_avatar.jpg')

    def __str__(self):
        return f'Profile of {self.user.username}'

    def get_absolute_uri(self):
        return reverse('profile', kwargs={"username": self.user.username})

class Following(models.Model):
    user_from = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='rel_from_set')
    user_to = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='rel_to_set')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-followed_at'])
        ]
        ordering = ['-followed_at']

user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self', through=Following, related_name='followers', symmetrical=False))