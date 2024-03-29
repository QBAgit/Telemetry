"""TELE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from Main import views
from django.conf.urls import include
from registration.views import loginUser, logoutUser, signup, activate

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.MainView.as_view(), name="index"),
    url(r'^api/v1/fdata/$', views.FdataListView.as_view()), 
    url(r'^api/v1/fdata/(?P<pk>[0-9]+)/$', views.FdataView.as_view()),
    url(r'^api/v1/usersensors/$', views.UserSensorList.as_view()),
    url(r'^api/v1/usersensors/(?P<pk>[0-9]+)/$', views.UserSensor.as_view()),
    url(r'^api/v1/sensordata/(?P<pk>[0-9]+)/$', views.SensorfData.as_view()),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

# Myapp user registration
urlpatterns += [
    path('login/',loginUser),
    path('logout/', logoutUser),
    path('signup/',signup),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
]
