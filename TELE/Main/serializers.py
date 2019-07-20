from rest_framework import serializers
from Main.models import Fdata
from registration.models import User


class FdataSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Fdata
        fields = ("id", "name", "description", "owner", "value")

class UserSerializer(serializers.ModelSerializer):
    Fdata = serializers.PrimaryKeyRelatedField(many=True, queryset=Fdata.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'Fdata')
