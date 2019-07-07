from django.db import models
from django.contrib.auth.models import User

class f_data(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    raw_value = models.CharField(max_length=32)
    eng_value = models.FloatField()
