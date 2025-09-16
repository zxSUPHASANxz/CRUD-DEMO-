from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

#
class Profile(models.Model):
    ROLE_CHOICES = [
        ("mechanic", "mechanic"),
        ("User", "User"),
    ]
    STATUS_CHOICES = [
        ("online", "online"),
        ("offline", "offline"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="User")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="offline")

    def __str__(self):
        return f"{self.user.username} ({self.role})"
