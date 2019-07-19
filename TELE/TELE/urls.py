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

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^tiny/$', views.TinyTest),
    url(r'^$', views.MainView.as_view(), name="index"),
    url(r'^login/$', views.UserLogin.as_view(), name="login"),
    url(r'^logout/$', views.UserLogout.as_view(), name="logout"),
    url(r'^api/v1/fdata/$', views.FdataListView.as_view()),
    url(r'^api/v1/fdata/(?P<pk>[0-9]+)/$', views.FdataView.as_view()),
    url(r'^api/v1/users/$', views.UserList.as_view()),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
