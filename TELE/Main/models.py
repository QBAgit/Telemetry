from django.db import models
from django.contrib.auth.models import User

class Fdata(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=140)
    owner = models.ForeignKey('registration.User', related_name='Fdata', on_delete=models.CASCADE)
    value = models.FloatField()
