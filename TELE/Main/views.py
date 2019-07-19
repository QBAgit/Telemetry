from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from Main.models import Fdata
from .serializers import FdataSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views, authenticate, login, logout
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import JsonResponse
from .forms import TinyFormTest

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


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
