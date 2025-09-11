from django.db import models

class Mechanic(models.Model):
    name = models.CharField(max_length=200)
    expertise = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
