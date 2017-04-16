from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import forms

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', auth_views.login, {'template_name':'login.html', 'authentication_form':forms.LoginForm},name='login'),
    url(r'^logout/', auth_views.logout, {'next_page':'/login'},name='logout'),
    url(r'^posts/',views.generateNewspaper,name='posts'),
]