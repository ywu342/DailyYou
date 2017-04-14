from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, User

# Create your views here.
def index(request):
    u = User.objects.get(username="yaling")
    u.rmCateFromUser('sports')
    #u.addCateToUser('sports')
    output = ','.join(u.getUserCates())
    return HttpResponse("All cates for yaling in db: "+output)

def profile(request):
    return HttpResponse("profile page")

def downloadPDF(request):
    return HttpResponse("download pdf page")

def generateNewspaper(request):
    return HttpResponse("Newspaper page")

# private helper functions to communicate with the db
def __addCateToUser(user_name, cate):
    u = User.objects.get(username=user_name)
    category = Category.objects.get(cate_name=cate)
    u.categories.add(category)
    
def __rmCateFromUser(user_name,cate):
    u = User.objects.get(username=user_name)
    category = Category.objects.get(cate_name=cate)
    u.categories.remove(category)
    
def __getUserCates(user_name):
    u = User.objects.get(username=user_name)
    qs = u.categories.all()
    categories = []
    for q in qs:
        categories.append(q.cate_name)
    return categories

def __getAllUser():
    latest_user_list = User.objects.all()
    output = ', '.join([u.username for u in latest_user_list])
    return output