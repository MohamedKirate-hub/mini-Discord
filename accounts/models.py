from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(null=True, blank=True)
    email = models.EmailField(unique=True)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"name: {self.first_name} {self.last_name}, username: {self.username}"
