from django.contrib import admin
from django.contrib.auth import views
from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', SignUpView.as_view(), name='logout')
]
