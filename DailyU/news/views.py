from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

# The index page is not allow to any view without authentication
@login_required(login_url="login/")
def index(request):
    return HttpResponse("This is the index page: Login")