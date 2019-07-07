from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import f_data

# Create your views here.

class MainView(View):
   def get(self, request):
       ctx = {"f_sensors": f_data.objects.all()}
       return render(request, "all_sensors.html",ctx)
