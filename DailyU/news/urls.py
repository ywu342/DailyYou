from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login,name='login'),
    url(r'^logout/', auth_views.logout, {'next_page':'/login'},name='logout'),
    url(r'^posts/$',views.newspaperIndex,name='sections'),
    url(r'^posts/(?P<section_name>[\w\-]+)/$',views.generateNewspaper,name='posts'),
    url(r'^editcat/', views.editCategory, name='editcat')
]