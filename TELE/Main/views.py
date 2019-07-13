from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from Main.models import Fdata
from .serializers import FdataSerializer
from django.contrib.auth.models import User
from rest_framework import generics
# Create your views here.

class MainView(View):
   def get(self, request):
       ctx = {"f_sensors": Fdata.objects.all()}
       return render(request, "all_sensors.html",ctx)


class FdataListView(generics.ListCreateAPIView):
    """Display all float measures"""
    queryset = Fdata.objects.all()
    serializer_class = FdataSerializer


class FdataView(generics.RetrieveUpdateDestroyAPIView):
    """Display float ID measure"""
    queryset = Fdata.objects.all()
    serializer_class = FdataSerializer
