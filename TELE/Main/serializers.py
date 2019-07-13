from rest_framework import serializers
from Main.models import Fdata
from django.contrib.auth.models import User


class FdataSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all())

    class Meta:
        model = Fdata
        fields = ("id", "name", "description", "owner", "raw_value", "eng_value")
