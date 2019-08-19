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
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Fdata.objects.all()
    serializer_class = FdataSerializer

    def create(self, request, *args, **kwargs):
        sensor_pk = request.POST['sensor']
        sensor_token = Sensor.objects.get(pk = sensor_pk).token
        req_token = request.POST['token']

        if req_token == sensor_token:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response("Sensor ID and Sensor Token do not match", status=status.HTTP_401_UNAUTHORIZED)


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
        queryset = self.filter_queryset(self.get_queryset()).filter(owner = request.user)
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
        sensorData = Fdata.objects.filter(sensor = sensor)

        try:
            start_date = request.GET["from"]
            end_date = request.GET["to"]
            sensorData = sensorData.filter(timestamp__gte = start_date, timestamp__lte = end_date)
        except MultiValueDictKeyError as e:
            print(e)
            try:
                start_date = request.GET["from"]
                sensorData = sensorData.filter(timestamp__gte = start_date)
            except MultiValueDictKeyError as e:
                print(e)
        
            try:
                end_date = request.GET["to"]
                sensorData = sensorData.filter(timestamp__lte = end_date)
            except MultiValueDictKeyError as e:
                print(e)

        finally:
            sensorData = sensorData.order_by('timestamp')
            serializer = FdataSerializer(sensorData, many = True)
            return Response(serializer.data)
    
    @staticmethod
    def parse_date(sdate):
        """
        Function parse date stored as string (yyyy-mm-dd) and return datetime.date object
        """
        from datetime import date
        std = sdate.split("-")
        return date(year = int(std[0]), month = int(std[1]), day = int(std[2]))