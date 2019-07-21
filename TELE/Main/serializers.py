from rest_framework import serializers
from Main.models import Fdata, Sensor
from registration.models import User


class FdataSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.email')
    sensor = serializers.ReadOnlyField(source='sensor.name')

    class Meta:
        model = Fdata
        fields = ("id", "sensor", "value")

class UserSensorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Sensor
        fields = ("id", "name", "description", "owner")

# class UserSerializer(serializers.ModelSerializer):
#     Fdata = serializers.PrimaryKeyRelatedField(many=True, queryset=Fdata.objects.all())

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'Fdata')
