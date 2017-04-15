from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import Category, User


# Create your views here.

# The index page is not allow to any view without authentication
@login_required(login_url="login/")
def index(request):
    cur_user = request.user
    print(cur_user.username)
    u = User.objects.get(username="yaling")
    u.addCateToUser('sports')
    print('***************test dbutils***************\n'+','.join(u.getUserCates()))
    u.rmCateFromUser('sports')
    output = ','.join(u.getUserCates())
    return render(request, "home.html")

def downloadPDF(request):
    return HttpResponse("download pdf page")

def generateNewspaper(request):
    return HttpResponse("Newspaper page")
