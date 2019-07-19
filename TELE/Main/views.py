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


def TinyTest(request):
    form = TinyFormTest
    if request.is_ajax():
        form = TinyFormTest(request.POST)
        if form.is_valid():
            data = {'msg':'sukces', 'form_data': form.cleaned_data}

            u = form.cleaned_data['name']
            p = form.cleaned_data['description']

            user = authenticate(username=u, password=p)

            if user is not None:
                # user authenticated
                login(request, user)
                data.update({"active_user":u, "login_status":"ok"})
            else:
                data.update({"login_status": "failed"})

            return JsonResponse(data)
    ctx = {'form': form}
    return render(request, "tiny.html",ctx)

class UserLogin(auth_views.LoginView):

    template_name = "login_user.html"
    redirect_field_name = "index"

    def form_invalid(self, form):
        response = super(UserLogin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(UserLogin  , self).form_valid(form)
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response


class UserLogout(View):

    def get(self, request):
        return render(request, "logout_user.html")

    def post(self, request):
        logout(request)
        return HttpResponseRedirect('/')

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
