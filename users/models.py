from django.db import models

from django.db import models
from PIL import Image

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    past_address = models.TextField()
    current_address = models.TextField()
    bio = models.TextField()


    def __str__(self):
        return self.user.username

