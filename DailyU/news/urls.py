from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login,name='login'),
    url(r'^logout/', auth_views.logout, {'next_page':'/login'},name='logout'),
    url(r'^editcat/', views.editCategory, name='editcat')
    
]