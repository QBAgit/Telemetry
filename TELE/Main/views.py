from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

# Create your views here.

class MainView(View):
   def get(self, request):
       return render(request, "base.html")
