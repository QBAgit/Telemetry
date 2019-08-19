from django.db import models
# from django.contrib.auth.models import User
from registration.models import User
# from django.utils.timezone import now
from hashlib import pbkdf2_hmac
from binascii import hexlify
from hmac import compare_digest

class Token():
    @staticmethod
    def generate(password, salt):
        AUTH_SIZE = 16
        byte_password = bytes(str(password),'utf-8')
        byte_salt = bytes(str(salt),'utf-8')
        dk = pbkdf2_hmac('sha256',byte_password, byte_salt, 100000, AUTH_SIZE)
        return hexlify(dk).decode('utf-8')


class SensorManager(models.Manager):
    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        
        obj_data['token'] = Token.generate(obj_data['name'], obj_data['description'])

        # Now call the super method which does the actual creation
        return super().create(**obj_data) # Python 3 syntax!!



class Sensor(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=140)
    owner = models.ForeignKey(User, related_name='Sensor', on_delete=models.CASCADE)
    token = models.CharField(max_length=32)

    objects = SensorManager()

    # @classmethod
    # def generate(cls):

    #     AUTH_SIZE = 16

    #     byte_sensor_name = bytes(str(cls.name),'utf-8')
    #     byte_description = bytes(str(cls.description),'utf-8')
    #     dk = pbkdf2_hmac('sha256',byte_sensor_name, byte_description, 100000, AUTH_SIZE)
    #     return hexlify(dk)

    # @classmethod
    # def verify(cls, sig):
    #     good_sig = Sensor.generate(senor_name, sensor_description)
    #     return compare_digest(good_sig, sig)

    # @classmethod
    # def create(cls, name, desc, owner):
    #     sensor = cls(name = name, description = desc, owner = owner)
    #     sensor.token = Sensor.generate()
    #     return sensor


class Fdata(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
