from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import Category, User
import sys


# Create your views here.

# The index page is not allow to any view without authentication
def getCurrentUser(request):
    username = request.session.get('current_user',None)
    if username is not None:
        user = User.objects.get(username =username )
    else:
        user = None
    return user

def check_login(orig_func):
    def temp_func(request):
        if getCurrentUser(request) == None:
            return HttpResponseRedirect("/login")
        else:
            return orig_func(request)
    return temp_func


@check_login
def index(request):
    cur_user = request.user
    print(cur_user.username)
    u = User.objects.get(username="yaling")
    u.addCateToUser('sports')
    print('***************test dbutils***************\n'+','.join(u.getUserCates()))
    u.rmCateFromUser('sports')
    output = ','.join(u.getUserCates())
    return render(request,"home.html")

def login(request):
    username = request.POST.get('username',False)
    password = request.POST.get('password',False)
    try:
        user = User.objects.get(username=username)
        if(str(user.password) == str(password)):
            request.session['current_user'] = user.username
            return render_to_response("home.html",{'user':user})
        else:
            return render_to_response("login.html",{'err':'login error',
                'user':None},\
                context_instance=RequestContext(request))
    except:
        e = sys.exc_info()[0]
        print(e)
    return render(request, "login.html")


def editCategory(request):
    return

def downloadPDF(request):
    return HttpResponse("download pdf page")

def generateNewspaper(request):
    return HttpResponse("Newspaper page")
