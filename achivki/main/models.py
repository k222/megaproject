from django.db import models
class UProfile(models.Model):
    name = models.CharField(max_length=75)
    password = models.CharField(max_length= 30)
    email = models.EmailField()
