from rest_framework import serializers
from Main.models import Fdata
from django.contrib.auth.models import User


class FdataSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # owner = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all())

    class Meta:
        model = Fdata
        fields = ("id", "name", "description", "owner", "value")

class UserSerializer(serializers.ModelSerializer):
    Fdata = serializers.PrimaryKeyRelatedField(many=True, queryset=Fdata.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'Fdata')
