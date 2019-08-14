from django.db import models
# from django.contrib.auth.models import User
from registration.models import User
# from django.utils.timezone import now

class Sensor(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=140)
    owner = models.ForeignKey(User, related_name='Sensor', on_delete=models.CASCADE)

class Fdata(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
