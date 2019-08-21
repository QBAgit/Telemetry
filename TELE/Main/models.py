from django.db import models
from registration.models import User
from Main.utilities import Token


class SensorManager(models.Manager):
    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # gengenerate sensor token
        
        obj_data['token'] = Token.generate(obj_data['name'], obj_data['description'])

        # Now call the super method which does the actual creation
        return super().create(**obj_data)


class Sensor(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=140)
    owner = models.ForeignKey(User, related_name='Sensor', on_delete=models.CASCADE)
    token = models.CharField(max_length=32)

    objects = SensorManager()


class Fdata(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
