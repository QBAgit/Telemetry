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
from django.utils.datastructures import MultiValueDictKeyError

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


class FdataView(generics.RetrieveUpdateDestroyAPIView):
    """Display float ID measure"""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Fdata.objects.all()
    serializer_class = FdataSerializer


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


class UserSensor(generics.RetrieveUpdateDestroyAPIView):
    """Display Sensor"""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Sensor.objects.all()
    serializer_class = UserSensorSerializer


class SensorfData(APIView):
    """Display all sensor data based on sensor ID"""

    def get(self, request, *args, **kwargs):
      
        sensor = get_object_or_404(Sensor, id=kwargs.pop("pk"))
        SensorData = Fdata.objects.filter(sensor = sensor)

        try:
            start_date = request.GET["from"]
            end_date = request.GET["to"]
            SensorData = SensorData.filter(timestamp__gte = start_date, timestamp__lte = end_date)
        except MultiValueDictKeyError as e:
            print(e)
            try:
                start_date = request.GET["from"]
                SensorData = SensorData.filter(timestamp__gte = start_date)
            except MultiValueDictKeyError as e:
                print(e)
        
            try:
                end_date = request.GET["to"]
                SensorData = SensorData.filter(timestamp__lte = end_date)
            except MultiValueDictKeyError as e:
                print(e)

        finally:
            SensorData = SensorData.order_by('timestamp')
            serializer = FdataSerializer(SensorData, many = True)
            return Response(serializer.data)
    
    @staticmethod
    def parse_date(sdate):
        """
        Function parse date stored as string (yyyy-mm-dd) and return datetime.date object
        """
        from datetime import date
        std = sdate.split("-")
        return date(year = int(std[0]), month = int(std[1]), day = int(std[2]))