from rest_framework import serializers
from Main.models import Fdata, Sensor
from registration.models import User


class UserSensorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Sensor
        fields = ("id", "name", "description", "owner")


class FdataSerializer(serializers.ModelSerializer):
    # sensor = serializers.ReadOnlyField(source='sensor.name')
    timestamp = serializers.ReadOnlyField()

    class Meta:
        model = Fdata
        fields = ("id", "sensor", "value", "timestamp")