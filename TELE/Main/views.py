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

# class add_f_data(View):
#     def post(self, request):
#         name = request.POST.get("name")
#         description = request.POST.get("description")
#         owner = request.POST.get("owner")
#         raw_value = request.POST.get("raw_value")
#
#         print("{}\t{}\t{}\t{}".format(name,description,owner,raw_value))
#
#         new_meas = f_data()
#         new_meas.name = name
#         new_meas.description = description
#         new_meas.owner = User.objects.get(name = owner)
#         new_meas.eng_value = float(raw_value)
#         new_meas.save()
#
#         return redirect("/")

class FdataListView(generics.ListCreateAPIView):
    """Display all float measures"""
    queryset = Fdata.objects.all()
    serializer_class = FdataSerializer

class FdataView(generics.RetrieveUpdateDestroyAPIView):
    """Display float ID measure"""
    queryset = Fdata.objects.all()
    serializer_class = FdataSerializer
