from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from Main.models import Fdata, Sensor
from .serializers import FdataSerializer, UserSensorSerializer
from registration.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import JsonResponse

from itertools import chain
# Create your views here.

class MainView(View):
   def get(self, request):
       ctx = {"f_sensors": Fdata.objects.all()}
       return render(request, "base.html",ctx)


class FdataListView(generics.ListCreateAPIView):
    """
    List all float measures or create a new measure
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Fdata.objects.all()
    serializer_class = FdataSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FdataView(generics.RetrieveUpdateDestroyAPIView):
    """Display float ID measure"""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Fdata.objects.all()
    serializer_class = FdataSerializer


class FuserDataView(APIView):
    """
    List User float measures , or create new one.
    """
    def get(self, request, format=None):
        # Get all user sensors
        UserSensors = Sensor.objects.filter(owner = request.user)

        ListQSets = []

        # Get all sensors data
        for sen in UserSensors:
            ListQSets.append(Fdata.objects.filter(sensor = sen))
        
        FUserData = list(chain(*ListQSets))

        serializer = FdataSerializer(FUserData, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FdataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSensorList(generics.ListCreateAPIView):
    """
    List all float measures or create a new measure
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Sensor.objects.all()
    serializer_class = UserSensorSerializer

    # override list metod from listModelMixin(object)
    # to show only logon user sensors

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.filter_queryset(Sensor.objects.filter(owner = request.user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SensorfData(APIView):
    """Display all sensor data by sensor ID"""

    def get(self, request, *args, **kwargs):
        sensor = get_object_or_404(Sensor, id=kwargs.pop("pk"))
        SensorData = Fdata.objects.filter(sensor = sensor)
        serializer = FdataSerializer(SensorData, many=True)
        return Response(serializer.data)