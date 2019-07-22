from django.db import models
from django.contrib.auth.models import User
from registration.models import User as RegUser
# from django.utils.timezone import now

class Sensor(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=140)
    owner = models.ForeignKey(RegUser, related_name='Sensor', on_delete=models.CASCADE)

class Fdata(models.Model):
    # name = models.CharField(max_length=32)
    # description = models.CharField(max_length=140)
    # owner = models.ForeignKey(User, related_name='Fdata', on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
