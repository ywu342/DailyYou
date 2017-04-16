from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import Category, User
from .webhoseUtil import WebhoseUtil
import os
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
    wh = WebhoseUtil()
    '''For development purpose, load existing json'''
    #wh.request("entertainment")
    file_path = os.path.join(os.path.dirname(__file__), 'test_jsons/sports.json')
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
    return render(request, "post_list.html", {'posts': posts})
