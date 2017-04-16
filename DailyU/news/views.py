from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import Category, User
#from el_pagination.views import AjaxListView
from .webhoseUtil import WebhoseUtil
import os
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

def newspaperIndex(request):
    cur_user = getCurrentUser(request)
    sections = cur_user.getUserCates()
    return render(request, "sections.html", {'sections':sections})

def generateNewspaper(request,section_name):#,page_template='post_list_page.html'):
    wh = WebhoseUtil()
    '''For development purpose, load existing json'''
    #print(section_name)
    #wh.request(section_name)
    file_path = os.path.join(os.path.dirname(__file__), 'test_jsons/'+section_name+'.json')
    wh.loadJson(file_path)
    posts = []
    for i in range(10):
        title = wh.getTitle(i)
        post_url = wh.getUrl(i)
        img = wh.getImg(i)
        text = wh.getText(i)
        author = wh.getAuthor(i)
        pub_time = wh.getPubTime(i)
        posts.append({"title": title,
                      "post_url": post_url,
                      "text": text,
                      "author": author,
                      "pub_time": pub_time})
    context = {
        'posts': posts,
        'section_name':section_name,
        #'page_template': page_template,
    }
#     if request.is_ajax():
#         template = page_template
    return render_to_response(
        "post_list.html", context, request)
    #return render(request, "post_list.html", {'posts': posts, 'section_name':section_name})
